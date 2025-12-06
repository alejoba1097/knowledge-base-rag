import { type ChangeEvent, useState } from 'react';

export type UploadStatus = 'idle' | 'uploading' | 'ready' | 'error';

export type UploadPanelProps = {
  file: File | null;
  status: UploadStatus;
  statusMessage?: string | null;
  onFileSelect: (file: File | null) => void;
  onUpload: () => Promise<void> | void;
};

export function UploadPanel({ file, status, statusMessage, onFileSelect, onUpload }: UploadPanelProps) {
  const [localError, setLocalError] = useState<string | null>(null);

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const nextFile = event.target.files?.[0];

    if (!nextFile) {
      onFileSelect(null);
      return;
    }

    if (nextFile.type !== 'application/pdf') {
      setLocalError('Only PDF files are supported right now.');
      onFileSelect(null);
      return;
    }

    setLocalError(null);
    onFileSelect(nextFile);
  };

  const handleUploadClick = () => {
    if (!file || status === 'uploading') return;
    void onUpload();
  };

  const renderStatus = () => {
    if (localError) return localError;
    if (statusMessage) return statusMessage;
    if (status === 'ready') return 'Indexed and ready for grounded Q&A.';
    if (status === 'uploading') return 'Uploading and indexing your PDF…';
    if (status === 'error') return 'Upload failed. Please try again.';
    return 'Drop a PDF or choose a file to start.';
  };

  const badgeText = () => {
    if (status === 'uploading') return 'Processing';
    if (status === 'ready') return 'Ready';
    if (status === 'error') return 'Needs retry';
    return 'Idle';
  };

  return (
    <section className="panel upload-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Document intake</p>
          <h2>Upload and index your PDF</h2>
          <p className="muted">The frontend handles uploads and hands off to your backend to chunk and embed.</p>
        </div>
        <span className={`status-badge status-${status}`}>{badgeText()}</span>
      </div>

      <label className="upload-dropzone" htmlFor="pdf-upload">
        <div className="upload-icon" aria-hidden>
          <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="5" y="5" width="38" height="38" rx="10" fill="var(--glass)" stroke="var(--accent-strong)" strokeWidth="2" />
            <path d="M24 13v22m0-22 8 8m-8-8-8 8" stroke="var(--accent-strong)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
            <path d="M14 35h20" stroke="var(--accent-strong)" strokeWidth="2.5" strokeLinecap="round" />
          </svg>
        </div>
        <div>
          <p className="upload-title">Drop your PDF here</p>
          <p className="muted">Or click to browse. Max 20MB for now.</p>
        </div>
        <input
          id="pdf-upload"
          name="pdf"
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          className="sr-only"
        />
      </label>

      {file && (
        <div className="file-chip" role="status">
          <div>
            <p className="file-name">{file.name}</p>
            <p className="muted">{formatSize(file.size)}</p>
          </div>
          <button type="button" className="ghost" onClick={() => onFileSelect(null)} aria-label="Remove file">
            Remove
          </button>
        </div>
      )}

      <div className="upload-actions">
        <div className="status-text">{renderStatus()}</div>
        <button
          type="button"
          className="primary"
          onClick={handleUploadClick}
          disabled={!file || status === 'uploading'}
        >
          {status === 'uploading' ? 'Uploading…' : status === 'ready' ? 'Re-upload' : 'Upload & Index'}
        </button>
      </div>
    </section>
  );
}

export default UploadPanel;
