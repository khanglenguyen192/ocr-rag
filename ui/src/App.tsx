import { useState, useMemo, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';
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
  const [streamProgress, setStreamProgress] = useState<{ page: number; total: number } | null>(null);

  // YouTube verify state
  type YoutubeLanguage = { language: string; language_code: string; is_generated: boolean };
  type YoutubeStep = 'input' | 'select-language' | 'done';
  const [youtubeStep, setYoutubeStep] = useState<YoutubeStep>('input');
  const [youtubeLanguages, setYoutubeLanguages] = useState<YoutubeLanguage[]>([]);
  const [selectedLanguage, setSelectedLanguage] = useState<string>('');
  const [verifying, setVerifying] = useState(false);

  // OCR engine selection (for pdf-scan and image modes)
  type OcrEngine = 'lighton' | 'easyocr' | 'paddleocr';
  const [ocrEngine, setOcrEngine] = useState<OcrEngine>('lighton');

  // Timing
  type TimingResult = { totalMs: number; label: string };
  const [elapsed, setElapsed] = useState<number>(0);          // realtime counter (ms)
  const [timing, setTiming] = useState<TimingResult | null>(null); // final result
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const startTimeRef = useRef<number>(0);

  const startTimer = () => {
    setElapsed(0);
    setTiming(null);
    startTimeRef.current = performance.now();
    timerRef.current = setInterval(() => {
      setElapsed(Math.round(performance.now() - startTimeRef.current));
    }, 100);
  };

  const stopTimer = (label: string) => {
    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = null;
    const totalMs = Math.round(performance.now() - startTimeRef.current);
    setElapsed(0);
    setTiming({ totalMs, label });
  };

  // Cleanup timer on unmount
  useEffect(() => () => { if (timerRef.current) clearInterval(timerRef.current); }, []);

  // File preview state
  const [imagePreviewUrl, setImagePreviewUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0] || null;
    setFile(f);
    // Tạo preview URL cho ảnh
    if (imagePreviewUrl) URL.revokeObjectURL(imagePreviewUrl);
    if (f && f.type.startsWith('image/')) {
      setImagePreviewUrl(URL.createObjectURL(f));
    } else {
      setImagePreviewUrl(null);
    }
  };

  const handleDeleteFile = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setFile(null);
    if (imagePreviewUrl) { URL.revokeObjectURL(imagePreviewUrl); setImagePreviewUrl(null); }
    // Reset input value để có thể chọn lại cùng file
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  // Cleanup preview URL on unmount
  useEffect(() => () => { if (imagePreviewUrl) URL.revokeObjectURL(imagePreviewUrl); }, []);
  const [leftWidth, setLeftWidth] = useState<number>(50); // percent
  const isDragging = useRef(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const onDividerMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    isDragging.current = true;
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';

    const onMouseMove = (ev: MouseEvent) => {
      if (!isDragging.current || !containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      const newLeft = ((ev.clientX - rect.left) / rect.width) * 100;
      setLeftWidth(Math.min(Math.max(newLeft, 20), 80)); // clamp 20%–80%
    };

    const onMouseUp = () => {
      isDragging.current = false;
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
    };

    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
  };

  // Detect if content is HTML or Markdown
  const contentType = useMemo<'html' | 'markdown'>(() => {
    if (!result) return 'markdown';
    const trimmed = result.trimStart();
    if (/^<!DOCTYPE\s/i.test(trimmed) || /^<(html|body|div|p|h[1-6]|ul|ol|table|span|article|section|main)\b/i.test(trimmed)) {
      return 'html';
    }
    return 'markdown';
  }, [result]);

  // Xử lý SSE stream (scanned PDF — trả về từng trang)
  const processSSEStream = async (response: Response, signal?: AbortSignal) => {
    setResult('');
    setStreamProgress(null);

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    if (!reader) return;

    let buffer = '';
    const pageTexts: string[] = [];
    const pageTimes: number[] = [];

    // Khi abort: cancel reader
    signal?.addEventListener('abort', () => { reader.cancel(); });

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        const parts = buffer.split('\n\n');
        buffer = parts.pop() ?? '';

        for (const part of parts) {
          const line = part.trim();
          if (!line.startsWith('data: ')) continue;

          try {
            const payload = JSON.parse(line.slice(6));

            if (payload.type === 'start') {
              setStreamProgress({ page: 0, total: payload.total });
            } else if (payload.type === 'page') {
              pageTexts.push(payload.text);
              if (payload.page_elapsed_ms) pageTimes.push(payload.page_elapsed_ms);
              setStreamProgress({ page: payload.page, total: payload.total });
              const merged = pageTexts
                .map((t, i) => `<!-- Trang ${i + 1} -->\n\n${t.trim()}`)
                .join('\n\n---\n\n');
              setResult(merged);
            } else if (payload.type === 'done') {
              setStreamProgress(null);
            } else if (payload.type === 'error') {
              setError(`Lỗi OCR: ${payload.message}`);
            }
          } catch {
            // ignore non-JSON lines
          }
        }
      }
    } catch (err: any) {
      if (err.name !== 'AbortError') {
        console.error('SSE stream reading error:', err);
        setError('Lỗi khi đọc dữ liệu từ server.');
      }
    } finally {
      setStreamProgress(null);
    }
  };

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

    // Tạo AbortController mới cho mỗi request
    const controller = new AbortController();
    abortControllerRef.current = controller;

    setLoading(true);
    setError('');
    setResult('');
    setJobId(null);
    setStreamProgress(null);
    startTimer();

    const labelMap = {
      'pdf-digital': 'PDF Digital (pymupdf4llm)',
      'pdf-scan':    `PDF Scan (${ocrEngine})`,
      'image':       `Image OCR (${ocrEngine})`,
    };

    const formData = new FormData();
    const endpointMap = {
      'pdf-digital': `${API_URL}/api/v1/pdf/digital`,
      'pdf-scan':    `${API_URL}/api/v1/pdf/scanned?engine=${ocrEngine}`,
      'image':       `${API_URL}/api/v1/ocr/image?engine=${ocrEngine}`,
    };
    const endpoint = endpointMap[uploadMode];

    formData.append('file', file);

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData,
        signal: controller.signal,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Upload failed: ${response.statusText} - ${errorText}`);
      }

      if (uploadMode === 'pdf-scan') {
        await processSSEStream(response, controller.signal);
      } else {
        await processStream(response);
      }

    } catch (err: any) {
      if (err.name === 'AbortError') {
        setError('');  // Huỷ bình thường, không hiện lỗi
      } else {
        setError(err.message || 'Có lỗi xảy ra khi xử lý file');
      }
    } finally {
      abortControllerRef.current = null;
      stopTimer(labelMap[uploadMode]);
      setLoading(false);
    }
  };

  const handleCancelUpload = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
  };

  const handleYoutubeVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!youtubeUrl) return;

    setVerifying(true);
    setError('');
    setYoutubeLanguages([]);
    setSelectedLanguage('');
    setYoutubeStep('input');
    startTimer();

    try {
      const response = await fetch(`${API_URL}/api/v1/youtube/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: youtubeUrl }),
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(err.detail || 'Không thể xác minh URL.');
      }

      const data = await response.json();
      const langs: YoutubeLanguage[] = data.available_languages ?? [];
      setYoutubeLanguages(langs);
      setSelectedLanguage(langs[0]?.language_code ?? '');
      setYoutubeStep('select-language');
    } catch (err: any) {
      setError(err.message);
    } finally {
      stopTimer('YouTube Verify');
      setVerifying(false);
    }
  };

  const handleYoutubeTranscript = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!youtubeUrl || !selectedLanguage) return;

    setLoading(true);
    setError('');
    setResult('');
    startTimer();

    try {
      const response = await fetch(`${API_URL}/api/v1/youtube/transcript`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: youtubeUrl, language_code: selectedLanguage }),
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(err.detail || 'Không thể lấy transcript.');
      }
      await processStream(response);
      setYoutubeStep('done'); // giữ nguyên list ngôn ngữ, chỉ reset khi bấm Huỷ
    } catch (err: any) {
      setError(err.message);
    } finally {
      stopTimer(`YouTube Transcript (${selectedLanguage})`);
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
      <div
        ref={containerRef}
        className="max-w-[1600px] mx-auto flex gap-0 h-[90vh]"
      >
        {/* LEFT COLUMN: Controls */}
        <div
          className="flex flex-col gap-6 overflow-y-auto pr-4 shrink-0"
          style={{ width: `${leftWidth}%` }}
        >
          <header className="mb-4">
            <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
              <FileText className="w-8 h-8 text-blue-600" />
              Convert2Text
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
                  {uploadMode === 'pdf-scan' && '🤖 OCR AI – phù hợp PDF scan không có text layer'}
                  {uploadMode === 'image' && '🤖 OCR AI – nhận diện văn bản từ ảnh'}
                </p>

                {/* OCR Engine Selector — chỉ hiện cho pdf-scan và image */}
                {(uploadMode === 'pdf-scan' || uploadMode === 'image') && (
                  <div className="bg-gray-50 rounded-lg p-3 space-y-2">
                    <p className="text-xs font-semibold text-gray-600 uppercase tracking-wide">OCR Engine</p>
                    <div className="grid grid-cols-3 gap-2">
                      {([
                        { value: 'lighton',   label: 'LightOn OCR', desc: 'AI 2-1B, tốt nhất' },
                        { value: 'easyocr',   label: 'EasyOCR',     desc: 'Nhanh, đa ngôn ngữ' },
                        { value: 'paddleocr', label: 'PaddleOCR',   desc: 'Baidu, chính xác cao' },
                      ] as { value: OcrEngine; label: string; desc: string }[]).map((eng) => (
                        <button
                          key={eng.value}
                          type="button"
                          onClick={() => setOcrEngine(eng.value)}
                          className={`flex flex-col items-center gap-0.5 p-2.5 rounded-lg border-2 text-xs font-medium transition-all ${
                            ocrEngine === eng.value
                              ? 'border-blue-600 bg-blue-50 text-blue-700'
                              : 'border-gray-200 text-gray-500 hover:border-gray-300 hover:bg-white'
                          }`}
                        >
                          <span className="font-semibold">{eng.label}</span>
                          <span className={`text-[10px] ${ocrEngine === eng.value ? 'text-blue-500' : 'text-gray-400'}`}>{eng.desc}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* File drop zone */}
                <div className="relative">
                  {/* Drop zone — click mở file dialog */}
                  <div
                    onClick={() => !loading && fileInputRef.current?.click()}
                    className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors relative
                      ${loading ? 'cursor-not-allowed opacity-60' : 'cursor-pointer hover:bg-gray-50'}
                      ${file ? 'border-blue-300 bg-blue-50/30' : 'border-gray-300'}
                    `}
                  >
                    <input
                      ref={fileInputRef}
                      type="file"
                      className="hidden"
                      onChange={handleFileChange}
                      accept={uploadMode === 'image' ? 'image/*' : 'application/pdf'}
                      disabled={loading}
                    />

                    {file ? (
                      <div className="space-y-2">
                        {/* Image preview thumbnail */}
                        {uploadMode === 'image' && imagePreviewUrl ? (
                          <div className="group relative inline-block">
                            <img
                              src={imagePreviewUrl}
                              alt="preview"
                              className="max-h-32 max-w-full mx-auto rounded-md object-contain shadow-sm"
                            />
                            {/* Hover full preview */}
                            <div className="hidden group-hover:flex absolute z-50 bottom-full left-1/2 -translate-x-1/2 mb-2 p-2 bg-white rounded-xl shadow-2xl border border-gray-200 pointer-events-none">
                              <img
                                src={imagePreviewUrl}
                                alt="full preview"
                                className="max-h-64 max-w-xs rounded-lg object-contain"
                              />
                            </div>
                          </div>
                        ) : (
                          /* PDF icon */
                          <div className="group relative inline-block">
                            <div className="w-14 h-16 mx-auto bg-red-50 border-2 border-red-200 rounded-lg flex flex-col items-center justify-center gap-1 shadow-sm">
                              <FileInput className="w-6 h-6 text-red-400" />
                              <span className="text-[10px] font-bold text-red-400 uppercase">PDF</span>
                            </div>
                            {/* Hover PDF tooltip */}
                            <div className="hidden group-hover:flex absolute z-50 bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg shadow-xl pointer-events-none whitespace-nowrap flex-col gap-1">
                              <span className="font-semibold">{file.name}</span>
                              <span className="text-gray-300">{(file.size / 1024).toFixed(1)} KB</span>
                            </div>
                          </div>
                        )}

                        {/* Filename + delete */}
                        <div className="flex items-center justify-center gap-2">
                          <span className="text-sm font-semibold text-blue-600 truncate max-w-[200px]">{file.name}</span>
                          <span className="text-xs text-gray-400">({(file.size / 1024).toFixed(1)} KB)</span>
                          {/* Nút xoá — dùng button riêng, KHÔNG nằm trong vùng click file */}
                        </div>
                      </div>
                    ) : (
                      <div className="flex flex-col items-center gap-2 text-gray-400 py-2">
                        {uploadMode === 'image'
                          ? <Image className="w-10 h-10 text-gray-300" />
                          : <FileInput className="w-10 h-10 text-gray-300" />
                        }
                        <span className="text-sm">
                          {uploadMode === 'image' ? 'Kéo thả hoặc click để chọn ảnh' : 'Kéo thả hoặc click để chọn file PDF'}
                        </span>
                        <span className="text-xs text-gray-300">
                          {uploadMode === 'image' ? 'PNG, JPG, WEBP...' : 'PDF'}
                        </span>
                      </div>
                    )}
                  </div>

                  {/* Nút xoá file — nằm NGOÀI drop zone, góc trên phải */}
                  {file && !loading && (
                    <button
                      type="button"
                      onMouseDown={handleDeleteFile}
                      className="absolute -top-2 -right-2 z-10 w-6 h-6 rounded-full bg-red-500 hover:bg-red-600 text-white flex items-center justify-center text-xs font-bold shadow-md transition-colors"
                      title="Xoá file"
                    >
                      ✕
                    </button>
                  )}
                </div>

                {/* Submit + Cancel buttons */}
                <div className="flex gap-2">
                  <button
                      disabled={!file || loading}
                      type="submit"
                      className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-semibold py-2.5 rounded-lg flex justify-center items-center gap-2 transition-all"
                  >
                      {loading
                        ? <><Loader2 className="animate-spin w-5 h-5"/>
                            Đang xử lý... {elapsed > 0 && <span className="ml-1 font-mono text-blue-100">{(elapsed / 1000).toFixed(1)}s</span>}
                          </>
                        : 'Bắt đầu xử lý'
                      }
                  </button>
                  {/* Nút Huỷ — chỉ hiện khi đang xử lý */}
                  {loading && (
                    <button
                      type="button"
                      onClick={handleCancelUpload}
                      className="px-4 py-2.5 rounded-lg border-2 border-red-300 text-red-500 hover:bg-red-50 hover:border-red-400 font-semibold text-sm transition-all"
                    >
                      Huỷ
                    </button>
                  )}
                </div>
              </form>
            )}

            {/* YouTube Form */}
            {activeTab === 'youtube' && (
              <div className="space-y-4">
                {/* Step 1: Input URL + Verify */}
                <form onSubmit={handleYoutubeVerify} className="space-y-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">YouTube URL</label>
                    <div className="flex gap-2">
                      <input
                        type="url"
                        required
                        placeholder="https://www.youtube.com/watch?v=..."
                        value={youtubeUrl}
                        disabled={youtubeStep === 'select-language' || youtubeStep === 'done'}
                        onChange={(e) => {
                          setYoutubeUrl(e.target.value);
                        }}
                        className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 outline-none transition-all disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed"
                      />
                      {/* Nút Huỷ — chỉ hiện sau khi verify */}
                      {(youtubeStep === 'select-language' || youtubeStep === 'done') && (
                        <button
                          type="button"
                          onClick={() => {
                            setYoutubeStep('input');
                            setYoutubeUrl('');
                            setYoutubeLanguages([]);
                            setSelectedLanguage('');
                            setResult('');
                            setTiming(null);
                            setError('');
                          }}
                          className="px-3 py-2 rounded-lg border-2 border-gray-300 text-gray-500 hover:border-red-400 hover:text-red-500 hover:bg-red-50 transition-all text-sm font-medium"
                          title="Huỷ và nhập URL mới"
                        >
                          ✕ Huỷ
                        </button>
                      )}
                    </div>
                  </div>

                  {/* Nút verify — ẩn sau khi đã verify */}
                  {youtubeStep === 'input' && (
                    <button
                      disabled={!youtubeUrl || verifying || loading}
                      type="submit"
                      className="w-full bg-gray-700 hover:bg-gray-800 disabled:bg-gray-300 text-white font-semibold py-2.5 rounded-lg flex justify-center items-center gap-2 transition-all"
                    >
                      {verifying
                        ? <><Loader2 className="animate-spin w-4 h-4" />
                            Đang kiểm tra... {elapsed > 0 && <span className="ml-1 font-mono text-gray-300">{(elapsed / 1000).toFixed(1)}s</span>}
                          </>
                        : <><Youtube className="w-4 h-4" /> Kiểm tra & Lấy danh sách ngôn ngữ</>
                      }
                    </button>
                  )}
                </form>

                {/* Step 2: Select language + Submit — giữ nguyên sau khi fetch */}
                {(youtubeStep === 'select-language' || youtubeStep === 'done') && youtubeLanguages.length > 0 && (
                  <form onSubmit={handleYoutubeTranscript} className="space-y-3 pt-3 border-t border-gray-100">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Chọn ngôn ngữ transcript
                        <span className="ml-2 text-xs text-gray-400">({youtubeLanguages.length} ngôn ngữ)</span>
                      </label>
                      <select
                        value={selectedLanguage}
                        onChange={(e) => setSelectedLanguage(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 outline-none transition-all bg-white"
                      >
                        {youtubeLanguages.map((lang) => (
                          <option key={lang.language_code} value={lang.language_code}>
                            {lang.language} ({lang.language_code}){lang.is_generated ? ' — auto' : ''}
                          </option>
                        ))}
                      </select>
                    </div>
                    <button
                      disabled={!selectedLanguage || loading}
                      type="submit"
                      className="w-full bg-red-600 hover:bg-red-700 disabled:bg-red-300 text-white font-semibold py-2.5 rounded-lg flex justify-center items-center gap-2 transition-all"
                    >
                      {loading
                        ? <><Loader2 className="animate-spin w-4 h-4" />
                            Đang lấy transcript... {elapsed > 0 && <span className="ml-1 font-mono text-red-100">{(elapsed / 1000).toFixed(1)}s</span>}
                          </>
                        : <><FileText className="w-4 h-4" /> Lấy Transcript</>
                      }
                    </button>
                  </form>
                )}
              </div>
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

        {/* ── Drag Divider ── */}
        <div
          onMouseDown={onDividerMouseDown}
          className="group w-2 shrink-0 flex items-center justify-center cursor-col-resize select-none relative mx-1"
          title="Kéo để thay đổi kích thước"
        >
          {/* Visual track */}
          <div className="w-px h-full bg-gray-200 group-hover:bg-blue-400 transition-colors duration-150" />
          {/* Handle knob */}
          <div className="absolute top-1/2 -translate-y-1/2 w-4 h-8 rounded-full bg-gray-300 group-hover:bg-blue-400 group-active:bg-blue-500 flex items-center justify-center gap-px transition-colors duration-150 shadow-sm">
            <span className="w-px h-4 bg-white/80 rounded-full" />
            <span className="w-px h-4 bg-white/80 rounded-full" />
          </div>
        </div>

        {/* RIGHT COLUMN: Result Viewer */}
        <div className="flex flex-col h-full bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden min-w-0 flex-1">
            <div className="p-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
                <div className="flex items-center gap-3 flex-wrap">
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
                  {/* Realtime timer while processing */}
                  {(loading || verifying) && elapsed > 0 && (
                    <span className="text-xs px-2 py-0.5 rounded-full bg-yellow-100 text-yellow-700 font-mono flex items-center gap-1">
                      <Loader2 className="w-3 h-3 animate-spin" />
                      {(elapsed / 1000).toFixed(1)}s
                    </span>
                  )}
                  {/* Final timing badge */}
                  {timing && !loading && !verifying && (
                    <span className="text-xs px-2 py-0.5 rounded-full bg-green-100 text-green-700 font-medium flex items-center gap-1" title={timing.label}>
                      ⏱ {timing.totalMs >= 1000 ? `${(timing.totalMs / 1000).toFixed(2)}s` : `${timing.totalMs}ms`}
                      <span className="text-green-500 max-w-[140px] truncate">— {timing.label}</span>
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
                      <button
                        onClick={() => { setResult(''); setTiming(null); setJobId(null); setError(''); }}
                        className="text-sm flex items-center gap-1.5 text-gray-400 hover:text-red-500 border border-gray-300 hover:border-red-300 px-3 py-1.5 rounded-md bg-white transition-all"
                        title="Xoá kết quả"
                      >
                        ✕ Xoá
                      </button>
                    </div>
                )}
            </div>

            <div className="flex-1 overflow-auto p-6 bg-white">
                {/* Progress bar — hiển thị khi đang stream (dù đã có kết quả trang đầu) */}
                {streamProgress && (
                  <div className="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <div className="flex justify-between text-xs text-blue-700 mb-1.5 font-medium">
                      <span className="flex items-center gap-1.5">
                        <Loader2 className="w-3 h-3 animate-spin" />
                        Đang OCR trang {streamProgress.page} / {streamProgress.total}
                        {elapsed > 0 && (
                          <span className="font-mono text-blue-500">({(elapsed / 1000).toFixed(1)}s)</span>
                        )}
                      </span>
                      <span>{Math.round((streamProgress.page / streamProgress.total) * 100)}%</span>
                    </div>
                    <div className="w-full bg-blue-200 rounded-full h-1.5">
                      <div
                        className="bg-blue-500 h-1.5 rounded-full transition-all duration-500"
                        style={{ width: `${Math.round((streamProgress.page / streamProgress.total) * 100)}%` }}
                      />
                    </div>
                  </div>
                )}
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
                      prose-p:text-gray-700 prose-p:leading-relaxed prose-p:whitespace-pre-wrap
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
                          remarkPlugins={[remarkGfm, remarkBreaks]}
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
                                {streamProgress ? (
                                  <>
                                    <p className="font-medium text-blue-600">
                                      Đang OCR trang {streamProgress.page} / {streamProgress.total}...
                                    </p>
                                    <div className="mt-3 w-48 bg-gray-200 rounded-full h-2">
                                      <div
                                        className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                                        style={{ width: `${Math.round((streamProgress.page / streamProgress.total) * 100)}%` }}
                                      />
                                    </div>
                                    <p className="text-xs mt-2 text-gray-400">
                                      {Math.round((streamProgress.page / streamProgress.total) * 100)}%
                                    </p>
                                  </>
                                ) : (
                                  <>
                                    <p>Đang xử lý dữ liệu...</p>
                                    <p className="text-xs mt-2">Dữ liệu sẽ hiện dần khi có kết quả.</p>
                                  </>
                                )}
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

