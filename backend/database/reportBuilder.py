'''
/database/reportBuilder.py
-> handle HTML report generation for CSV fetch
'''

class ReportBuilder:
    def __init__(self):
        self.report = ""
        self.unchangedStart = None
        self.unchangedEnd = None
        self.nanStart = None
        self.nanEnd = None

    def getStyles(self):
        return """
        <style>
            /* CSS Reset */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            /* Color palette matching frontend */
            :root {
                --color-color-1: #e0e0e0;
                --color-color-2: #9a9a9a;
                --color-color-bg: #080808;
                --color-success: #27ae60;
                --color-info: #3498db;
                --color-warning: #f39c12;
                --color-error: #e74c3c;
            }

            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Geist', 'Segoe UI', system-ui, sans-serif;
                max-width: 1400px;
                margin: 0 auto;
                padding: 5.25rem 3.75rem;
                background-color: var(--color-color-bg);
                color: var(--color-color-1);
                line-height: 1.6;
            }

            @media (max-width: 768px) {
                body {
                    padding: 5.25rem 1.25rem;
                }
            }

            h1 {
                font-size: 48px;
                font-weight: 700;
                color: var(--color-color-1);
                border-bottom: 2px solid var(--color-color-2);
                padding-bottom: 1rem;
                margin-bottom: 1.5rem;
                letter-spacing: -0.02em;
            }

            h3 {
                font-size: 24px;
                font-weight: 700;
                color: var(--color-color-1);
                margin-top: 2rem;
                margin-bottom: 1rem;
            }

            span {
                display: block;
                padding: 0.75rem 1rem;
                margin: 0.5rem 0;
                background-color: rgba(224, 224, 224, 0.05);
                border-left: 3px solid var(--color-color-2);
                border-radius: 4px;
                font-size: 16px;
                transition: all 0.2s ease;
            }

            span:hover {
                background-color: rgba(224, 224, 224, 0.08);
            }

            /* Different colors for different message types */
            span:has(Error) {
                border-left-color: var(--color-error);
                background-color: rgba(231, 76, 60, 0.1);
                color: #ff6b6b;
            }

            span:has(Error):hover {
                background-color: rgba(231, 76, 60, 0.15);
            }

            span:has(Created) {
                border-left-color: var(--color-success);
                background-color: rgba(39, 174, 96, 0.1);
                color: #51cf66;
            }

            span:has(Created):hover {
                background-color: rgba(39, 174, 96, 0.15);
            }

            span:has(Updated) {
                border-left-color: var(--color-info);
                background-color: rgba(52, 152, 219, 0.1);
                color: #4dabf7;
            }

            span:has(Updated):hover {
                background-color: rgba(52, 152, 219, 0.15);
            }

            span:has(nan), span:has(not a valid link) {
                border-left-color: var(--color-warning);
                background-color: rgba(243, 156, 18, 0.1);
                color: #ffa94d;
            }

            span:has(nan):hover, span:has(not a valid link):hover {
                background-color: rgba(243, 156, 18, 0.15);
            }

            /* Links styling */
            a {
                color: var(--color-info);
                text-decoration: none;
                transition: opacity 0.2s ease;
            }

            a:hover {
                opacity: 0.8;
                text-decoration: underline;
            }

            /* Code/monospace elements */
            code {
                font-family: 'GeistMono', 'Courier New', monospace;
                font-size: 14px;
                background-color: rgba(224, 224, 224, 0.1);
                padding: 0.2rem 0.4rem;
                border-radius: 3px;
            }
        </style>
        """
    
    def appendMessage(self, msg):
        self.report = self.report + '\n' + msg
    
    def initialize(self, total_lines):
        self.report = self.getStyles()
        self.report += f"<h1>CSV carregado com sucesso!</h1><h3>{total_lines} linhas encontradas.</h3>"
        self.unchangedStart = self.unchangedEnd = None
        self.nanStart = self.nanEnd = None
    
    def flushUnchangedBatch(self):
        if self.unchangedStart is not None:
            if self.unchangedStart == self.unchangedEnd:
                self.appendMessage(f"<span>Sem alterações na linha {self.unchangedStart}.<br></span>")
            else:
                self.appendMessage(f"<span>Sem alterações nas linhas {self.unchangedStart} a {self.unchangedEnd}.<br></span>")
            self.unchangedStart = self.unchangedEnd = None
    
    def flushNanBatch(self):
        if self.nanStart is not None:
            if self.nanStart == self.nanEnd:
                self.appendMessage(f"<span>Linha {self.nanStart} — link inválido (nan).<br></span>")
            else:
                self.appendMessage(f"<span>Linhas {self.nanStart} a {self.nanEnd} — link inválido (nan).<br></span>")
            self.nanStart = self.nanEnd = None
    
    def resetUnchangedBoundaries(self):
        self.unchangedStart = self.unchangedEnd = None
    
    def addNanLine(self, line_index):
        self.flushUnchangedBatch()
        if self.nanStart is None:
            self.nanStart = line_index
        self.nanEnd = line_index
    
    def addUnchangedLine(self, line_index):
        if self.unchangedStart is None:
            self.unchangedStart = line_index
        self.unchangedEnd = line_index
    
    def addInvalidLink(self, line_index, link):
        self.flushUnchangedBatch()
        self.flushNanBatch()
        self.appendMessage(f"<span>Linha {line_index} — link inválido ({link}).<br></span>")
        self.resetUnchangedBoundaries()
    
    def addError(self, line_index, pid, error_msg):
        self.flushUnchangedBatch()
        self.resetUnchangedBoundaries()
        self.flushNanBatch()
        self.appendMessage(f"<span>Linha {line_index} — Erro: {pid} — {error_msg}.<br></span>")
    
    def addCreatedProject(self, line_index, pid):
        self.appendMessage(f"<span>Linha {line_index} — Criado novo projeto: {pid}.<br></span>")
    
    def addUpdatedProject(self, line_index, pid, changes):
        self.flushUnchangedBatch()
        self.appendMessage(f"<span>Linha {line_index} — Atualizado {pid}: {', '.join(changes)}.<br></span>")
    
    def addDuplicateSummary(self, duplicate_ids):
        if not duplicate_ids:
            return

        self.appendMessage(f"<h3>Resumo de Duplicados:</h3>")

        for pid, lines in duplicate_ids.items():
            if len(lines) == 2:
                self.appendMessage(f"<span>- https://vimeo.com/{pid} repetido nas linhas {lines[0]} e {lines[1]}<br></span>")
            else:
                lines_str = ', '.join(map(str, lines[:-1])) + f" e {lines[-1]}"
                self.appendMessage(f"<span>- https://vimeo.com/{pid} repetido nas linhas {lines_str}<br></span>")
    
    def addDatabaseSummary(self, total_projects):
        self.appendMessage(f"<h3>{total_projects} objetos na base de dados.</h3>")
    
    def finalize(self):
        self.flushUnchangedBatch()
        self.flushNanBatch()
        return self.report