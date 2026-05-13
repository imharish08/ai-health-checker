from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'HealthCheck AI - Project Documentation', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 8, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, body)
        self.ln()

def create_pdf():
    pdf = PDF()
    pdf.add_page()

    pdf.chapter_title('1. Project Overview')
    pdf.chapter_body('HealthCheck AI is a lightweight, full-stack medical symptom checker. It leverages Machine Learning (Random Forest) to analyze user-provided symptoms and predict potential diseases. The application is designed with a modern glassmorphism UI.')

    pdf.chapter_title('2. Tech Stack')
    pdf.chapter_body('- Backend: FastAPI (Python)\n- Machine Learning: Scikit-Learn (Random Forest)\n- Frontend: HTML5, CSS3, JavaScript (Vanilla)\n- Database: Browser LocalStorage (History Tracking)')

    pdf.chapter_title('3. Key Features')
    pdf.chapter_body('1. Symptom Input: Tag-based selection with suggestions.\n2. AI Prediction: Predicts diseases with confidence %.\n3. Clinical Metadata: Shows severity, precautions, and health tips.\n4. Local History: Stores past diagnostics locally.')

    pdf.chapter_title('4. Installation & Setup')
    pdf.chapter_body('1. Ensure Python 3.8+ is installed.\n2. Run: pip install fastapi uvicorn scikit-learn pandas numpy\n3. Run the project: ./run.ps1\n4. Access at: http://localhost:3000')

    pdf.chapter_title('5. File Structure')
    pdf.chapter_body('- backend/: Logic and ML models\n- frontend/: Web interface\n- data/: CSV and Metadata\n- run.ps1: Startup script')

    pdf.chapter_title('6. Disclaimer')
    pdf.chapter_body('For educational purposes only. Not a medical diagnosis tool. Consult a doctor for medical advice.')

    pdf.output('HealthCheck_AI_Documentation.pdf')
    print("PDF Generated successfully as HealthCheck_AI_Documentation.pdf")

if __name__ == "__main__":
    create_pdf()
