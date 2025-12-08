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
            body {
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 20px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }
            h3 {
                color: #34495e;
                margin-top: 20px;
            }
            span {
                display: block;
                padding: 5px 10px;
                margin: 3px 0;
                background-color: white;
                border-left: 3px solid #95a5a6;
                border-radius: 3px;
            }
            /* Different colors for different message types */
            span:has(Error) {
                border-left-color: #e74c3c;
                background-color: #ffebee;
            }
            span:has(Created) {
                border-left-color: #27ae60;
                background-color: #e8f5e9;
            }
            span:has(Updated) {
                border-left-color: #3498db;
                background-color: #e3f2fd;
            }
            span:has(nan) {
                border-left-color: #f39c12;
                background-color: #fff3e0;
            }
        </style>
        """
    
    def appendMessage(self, msg):
        self.report = self.report + '\n' + msg
    
    def initialize(self, total_lines):
        self.report = self.getStyles()
        self.report += f"<h1>CSV fetched with success!</h1><h3> {total_lines} lines found.</h3>"
        self.unchangedStart = self.unchangedEnd = None
        self.nanStart = self.nanEnd = None
    
    def flushUnchangedBatch(self):
        if self.unchangedStart is not None:
            if self.unchangedStart == self.unchangedEnd:
                self.appendMessage(f"<span>No changes at line {self.unchangedStart}.<br></span>")
            else:
                self.appendMessage(f"<span>No changes lines {self.unchangedStart} to {self.unchangedEnd}.<br></span>")
            self.unchangedStart = self.unchangedEnd = None
    
    def flushNanBatch(self):
        if self.nanStart is not None:
            if self.nanStart == self.nanEnd:
                self.appendMessage(f"<span>Line {self.nanStart} — not a valid link (nan).<br></span>")
            else:
                self.appendMessage(f"<span>Lines {self.nanStart} to {self.nanEnd} — not a valid link (nan).<br></span>")
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
        self.appendMessage(f"<span>Line {line_index} — not a valid link ({link}).<br></span>")
        self.resetUnchangedBoundaries()
    
    def addError(self, line_index, pid, error_msg):
        self.flushUnchangedBatch()
        self.resetUnchangedBoundaries()
        self.flushNanBatch()
        self.appendMessage(f"<span>Line {line_index} — Error: {pid} — {error_msg}.<br></span>")
    
    def addCreatedProject(self, line_index, pid):
        self.appendMessage(f"<span>Line {line_index} — Created new project: {pid}.<br></span>")
    
    def addUpdatedProject(self, line_index, pid, changes):
        self.flushUnchangedBatch()
        self.appendMessage(f"<span>Line {line_index} — Updated {pid}: {', '.join(changes)}.<br></span>")
    
    def addDuplicateSummary(self, duplicate_ids):
        if not duplicate_ids:
            return
        
        self.appendMessage(f"<h3>Duplicate Summary:</h3>")
        
        for pid, lines in duplicate_ids.items():
            if len(lines) == 2:
                self.appendMessage(f"<span>- https://vimeo.com/{pid} repeated at lines {lines[0]} and {lines[1]}<br></span>")
            else:
                lines_str = ', '.join(map(str, lines[:-1])) + f" and {lines[-1]}"
                self.appendMessage(f"<span>- https://vimeo.com/{pid} repeated at lines {lines_str}<br></span>")
    
    def addDatabaseSummary(self, total_projects):
        self.appendMessage(f"<h3>{total_projects} objects on the database.</h3>")
    
    def finalize(self):
        self.flushUnchangedBatch()
        self.flushNanBatch()
        return self.report