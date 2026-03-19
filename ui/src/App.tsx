import { useState, useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import rehypeRaw from 'rehype-raw';
import rehypeSanitize, { defaultSchema } from 'rehype-sanitize';
import 'highlight.js/styles/github.css';
import { Upload, Youtube, FileText, Download, Loader2, AlertCircle, Image, ScanLine, FileInput, Code, Eye } from 'lucide-react';

// Cấu hình URL backend (đổi nếu cần)
const API_URL = 'http://localhost:8000';

function App() {
  const [activeTab, setActiveTab] = useState<'upload' | 'youtube'>('upload');
  const [uploadMode, setUploadMode] = useState<'pdf-digital' | 'pdf-scan' | 'image'>('pdf-digital');
  const [file, setFile] = useState<File | null>(null);
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [jobId, setJobId] = useState<number | null>(null);
  const [viewMode, setViewMode] = useState<'preview' | 'raw'>('preview');

  // Detect if content is HTML or Markdown
  const contentType = useMemo<'html' | 'markdown'>(() => {
    if (!result) return 'markdown';
    const trimmed = result.trimStart();
    // Consider HTML if it starts with a tag or has common html structure
    if (/^<!DOCTYPE\s/i.test(trimmed) || /^<(html|body|div|p|h[1-6]|ul|ol|table|span|article|section|main)\b/i.test(trimmed)) {
      return 'html';
    }
    return 'markdown';
  }, [result]);

  // Xử lý Streaming response (Chuẩn bị cho tính năng load từng page)
  const processStream = async (response: Response) => {
    setResult(''); // Reset kết quả cũ

    // Nếu Backend chưa hỗ trợ stream mà trả JSON 1 cục, ta handle fallback
    // PHẢI check content-type TRƯỚC khi getReader() để tránh lock body stream
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
        const data = await response.json();
        // Giả sử API trả về { result_md: "...", id: ... }
        setResult(data.result_md || "");
        setJobId(data.id);
        return;
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) return;

    // Loop đọc stream
    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        // Cập nhật UI ngay khi có data mới
        setResult((prev) => prev + chunk);
      }
    } catch (err) {
      console.error("Stream reading error:", err);
      setError("Lỗi khi đọc dữ liệu từ server.");
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError('');
    setResult('');
    setJobId(null);

    const formData = new FormData();
    // Chọn endpoint dựa theo uploadMode
    const endpointMap = {
      'pdf-digital': `${API_URL}/api/v1/pdf/digital`,
      'pdf-scan':    `${API_URL}/api/v1/pdf/scanned`,
      'image':       `${API_URL}/api/v1/ocr/image`,
    };
    const endpoint = endpointMap[uploadMode];

    formData.append('file', file);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Upload failed: ${response.statusText} - ${errorText}`);
      }
      await processStream(response);

    } catch (err: any) {
      setError(err.message || 'Có lỗi xảy ra khi xử lý file');
    } finally {
      setLoading(false);
    }
  };

  const handleYoutube = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!youtubeUrl) return;

    setLoading(true);
    setError('');
    setResult('');

    try {
      const response = await fetch(`${API_URL}/api/v1/youtube/transcript`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: youtubeUrl }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to get transcript: ${response.statusText} - ${errorText}`);
      }
      await processStream(response);

    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const downloadMarkdown = () => {
    const blob = new Blob([result], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = jobId ? `job_${jobId}_result.md` : 'result.md';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans text-gray-800">
      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8 h-[90vh]">

        {/* LEFT COLUMN: Controls */}
        <div className="flex flex-col gap-6">
          <header className="mb-4">
            <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
              <FileText className="w-8 h-8 text-blue-600" />
              OCR Web Platform
            </h1>
            <p className="text-gray-500 mt-2">Convert Tool - PDF, Image & YouTube</p>
          </header>

          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            {/* Tabs */}
            <div className="flex gap-4 border-b border-gray-200 mb-6">
              <button
                type="button"
                onClick={() => setActiveTab('upload')}
                className={`pb-3 px-1 font-medium text-sm flex items-center gap-2 border-b-2 transition-colors ${
                  activeTab === 'upload' 
                    ? 'border-blue-600 text-blue-600' 
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <Upload className="w-4 h-4" /> Upload File
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('youtube')}
                className={`pb-3 px-1 font-medium text-sm flex items-center gap-2 border-b-2 transition-colors ${
                  activeTab === 'youtube' 
                    ? 'border-red-600 text-red-600' 
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <Youtube className="w-4 h-4" /> YouTube Transcript
              </button>
            </div>

            {/* Upload Form */}
            {activeTab === 'upload' && (
              <form onSubmit={handleUpload} className="space-y-4">

                {/* Mode Selector */}
                <div className="grid grid-cols-3 gap-2">
                  <button
                    type="button"
                    onClick={() => { setUploadMode('pdf-digital'); setFile(null); }}
                    className={`flex flex-col items-center gap-1.5 p-3 rounded-lg border-2 text-xs font-medium transition-all ${
                      uploadMode === 'pdf-digital'
                        ? 'border-blue-600 bg-blue-50 text-blue-700'
                        : 'border-gray-200 text-gray-500 hover:border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    <FileInput className="w-5 h-5" />
                    PDF Digital
                  </button>
                  <button
                    type="button"
                    onClick={() => { setUploadMode('pdf-scan'); setFile(null); }}
                    className={`flex flex-col items-center gap-1.5 p-3 rounded-lg border-2 text-xs font-medium transition-all ${
                      uploadMode === 'pdf-scan'
                        ? 'border-blue-600 bg-blue-50 text-blue-700'
                        : 'border-gray-200 text-gray-500 hover:border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    <ScanLine className="w-5 h-5" />
                    PDF Scan
                  </button>
                  <button
                    type="button"
                    onClick={() => { setUploadMode('image'); setFile(null); }}
                    className={`flex flex-col items-center gap-1.5 p-3 rounded-lg border-2 text-xs font-medium transition-all ${
                      uploadMode === 'image'
                        ? 'border-blue-600 bg-blue-50 text-blue-700'
                        : 'border-gray-200 text-gray-500 hover:border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    <Image className="w-5 h-5" />
                    Image
                  </button>
                </div>

                {/* Mode description badge */}
                <p className="text-xs text-gray-400 text-center -mt-1">
                  {uploadMode === 'pdf-digital' && '⚡ Dùng pymupdf4llm – nhanh, phù hợp PDF có text layer'}
                  {uploadMode === 'pdf-scan' && '🤖 Dùng AI 1B – phù hợp PDF scan không có text layer'}
                  {uploadMode === 'image' && '🤖 Dùng AI 1B – nhận diện văn bản từ ảnh'}
                </p>

                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:bg-gray-50 transition-colors cursor-pointer relative">
                    <input
                        type="file"
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                        onChange={(e) => setFile(e.target.files?.[0] || null)}
                        accept={uploadMode === 'image' ? 'image/*' : 'application/pdf'}
                    />
                    <div className="flex flex-col items-center justify-center gap-2 text-gray-500">
                        {uploadMode === 'image'
                          ? <Image className="w-10 h-10 text-gray-300" />
                          : <FileInput className="w-10 h-10 text-gray-300" />
                        }
                        {file ? (
                            <span className="font-semibold text-blue-600">{file.name}</span>
                        ) : (
                            <span>
                              {uploadMode === 'image'
                                ? 'Kéo thả hoặc click để chọn ảnh'
                                : 'Kéo thả hoặc click để chọn file PDF'
                              }
                            </span>
                        )}
                    </div>
                </div>
                <button
                    disabled={!file || loading}
                    type="submit"
                    className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-semibold py-2.5 rounded-lg flex justify-center items-center gap-2 transition-all"
                >
                    {loading ? <Loader2 className="animate-spin w-5 h-5"/> : 'Bắt đầu xử lý'}
                </button>
              </form>
            )}

            {/* YouTube Form */}
            {activeTab === 'youtube' && (
              <form onSubmit={handleYoutube} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">YouTube URL</label>
                  <input
                    type="url"
                    required
                    placeholder="https://www.youtube.com/watch?v=..."
                    value={youtubeUrl}
                    onChange={(e) => setYoutubeUrl(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 outline-none transition-all"
                  />
                </div>
                <button
                    disabled={!youtubeUrl || loading}
                    type="submit"
                    className="w-full bg-red-600 hover:bg-red-700 disabled:bg-red-300 text-white font-semibold py-2.5 rounded-lg flex justify-center items-center gap-2 transition-all"
                >
                    {loading ? <Loader2 className="animate-spin w-5 h-5"/> : 'Lấy Transcript'}
                </button>
              </form>
            )}

            {error && (
              <div className="mt-4 p-3 bg-red-50 text-red-700 rounded-lg flex items-center gap-2 text-sm">
                <AlertCircle className="w-4 h-4" /> {error}
              </div>
            )}
          </div>

            {/* Tips / Info */}
          <div className="bg-blue-50 p-4 rounded-lg text-sm text-blue-800">
            <h4 className="font-semibold mb-1">Note:</h4>
            <ul className="list-disc pl-5 space-y-1">
                <li>Hệ thống ưu tiên xử lý PDF Digital bằng `pymupdf4llm` (siêu nhanh).</li>
                <li>Ảnh và PDF Scan sẽ dùng Model AI 1B (chậm hơn, cần GPU).</li>
                <li>Code UI này hỗ trợ Streaming Response (SSE style).</li>
            </ul>
          </div>
        </div>

        {/* RIGHT COLUMN: Result Viewer */}
        <div className="flex flex-col h-full bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="p-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
                <div className="flex items-center gap-3">
                  <h2 className="font-semibold text-gray-700">Preview</h2>
                  {result && (
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                      contentType === 'html'
                        ? 'bg-orange-100 text-orange-700'
                        : 'bg-blue-100 text-blue-700'
                    }`}>
                      {contentType === 'html' ? 'HTML' : 'Markdown'}
                    </span>
                  )}
                </div>
                {result && (
                    <div className="flex items-center gap-2">
                      {/* Raw / Preview toggle */}
                      <div className="flex rounded-md border border-gray-300 overflow-hidden bg-white">
                        <button
                          onClick={() => setViewMode('preview')}
                          className={`text-xs flex items-center gap-1 px-2.5 py-1.5 transition-all ${
                            viewMode === 'preview'
                              ? 'bg-blue-600 text-white'
                              : 'text-gray-600 hover:bg-gray-50'
                          }`}
                        >
                          <Eye className="w-3.5 h-3.5" /> Preview
                        </button>
                        <button
                          onClick={() => setViewMode('raw')}
                          className={`text-xs flex items-center gap-1 px-2.5 py-1.5 border-l border-gray-300 transition-all ${
                            viewMode === 'raw'
                              ? 'bg-blue-600 text-white'
                              : 'text-gray-600 hover:bg-gray-50'
                          }`}
                        >
                          <Code className="w-3.5 h-3.5" /> Raw
                        </button>
                      </div>
                      <button
                        onClick={downloadMarkdown}
                        className="text-sm flex items-center gap-1.5 text-gray-600 hover:text-blue-600 border border-gray-300 px-3 py-1.5 rounded-md bg-white hover:border-blue-400 transition-all"
                      >
                          <Download className="w-4 h-4" /> Download .md
                      </button>
                    </div>
                )}
            </div>

            <div className="flex-1 overflow-auto p-6 bg-white">
                {result ? (
                  viewMode === 'raw' ? (
                    /* ── RAW view: VS Code-like source editor ── */
                    <pre className="text-xs font-mono text-gray-700 bg-gray-50 p-4 rounded-lg border border-gray-200 whitespace-pre-wrap break-words leading-relaxed h-full overflow-auto">
                      {result}
                    </pre>
                  ) : contentType === 'html' ? (
                    /* ── HTML preview: sandboxed iframe style ── */
                    <div
                      className="prose prose-sm sm:prose-base prose-blue max-w-none
                        prose-headings:font-bold prose-headings:text-gray-900
                        prose-h1:text-2xl prose-h2:text-xl prose-h3:text-lg
                        prose-p:text-gray-700 prose-p:leading-relaxed
                        prose-a:text-blue-600 prose-a:no-underline hover:prose-a:underline
                        prose-strong:text-gray-900
                        prose-code:bg-gray-100 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:text-sm prose-code:text-pink-600 prose-code:before:content-none prose-code:after:content-none
                        prose-pre:bg-gray-900 prose-pre:rounded-xl prose-pre:shadow-md prose-pre:p-0
                        prose-blockquote:border-l-4 prose-blockquote:border-blue-400 prose-blockquote:bg-blue-50 prose-blockquote:rounded-r-lg prose-blockquote:text-gray-600 prose-blockquote:not-italic
                        prose-table:text-sm prose-th:bg-gray-100 prose-th:font-semibold
                        prose-img:rounded-lg prose-img:shadow-sm
                        prose-hr:border-gray-200
                        prose-li:text-gray-700"
                      dangerouslySetInnerHTML={{ __html: result }}
                    />
                  ) : (
                    /* ── MARKDOWN preview (với rehype-raw hỗ trợ HTML inline) ── */
                    <article className="prose prose-sm sm:prose-base prose-blue max-w-none
                      prose-headings:font-bold prose-headings:text-gray-900
                      prose-h1:text-2xl prose-h2:text-xl prose-h3:text-lg
                      prose-p:text-gray-700 prose-p:leading-relaxed
                      prose-a:text-blue-600 prose-a:no-underline hover:prose-a:underline
                      prose-strong:text-gray-900
                      prose-code:bg-gray-100 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:text-sm prose-code:text-pink-600 prose-code:before:content-none prose-code:after:content-none
                      prose-pre:bg-gray-900 prose-pre:rounded-xl prose-pre:shadow-md prose-pre:p-0
                      prose-blockquote:border-l-4 prose-blockquote:border-blue-400 prose-blockquote:bg-blue-50 prose-blockquote:rounded-r-lg prose-blockquote:text-gray-600 prose-blockquote:not-italic
                      prose-table:text-sm prose-th:bg-gray-100 prose-th:font-semibold
                      prose-img:rounded-lg prose-img:shadow-sm
                      prose-hr:border-gray-200
                      prose-li:text-gray-700"
                    >
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          rehypePlugins={[
                            rehypeRaw,
                            [rehypeSanitize, {
                              ...defaultSchema,
                              attributes: {
                                ...defaultSchema.attributes,
                                '*': [...(defaultSchema.attributes?.['*'] ?? []), 'className', 'style'],
                                'code': [...(defaultSchema.attributes?.['code'] ?? []), 'className'],
                              }
                            }],
                            rehypeHighlight,
                          ]}
                        >
                          {result}
                        </ReactMarkdown>
                    </article>
                  )
                ) : (
                    <div className="h-full flex flex-col items-center justify-center text-gray-400">
                        {loading ? (
                            <>
                                <Loader2 className="w-10 h-10 animate-spin mb-4 text-blue-500" />
                                <p>Đang xử lý dữ liệu...</p>
                                <p className="text-xs mt-2">Dữ liệu sẽ hiện dần khi có kết quả.</p>
                            </>
                        ) : (
                            <>
                                <FileText className="w-16 h-16 mb-4 opacity-20" />
                                <p>Kết quả sẽ hiển thị tại đây</p>
                            </>
                        )}
                    </div>
                )}
            </div>
        </div>
      </div>
    </div>
  );
}

export default App;

