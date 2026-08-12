from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from app.pdf import generate_ticket_pdf
from app.schemas import TicketPDFRequest

app = FastAPI()


@app.post("/generate-ticket")
def generate_ticket(data: TicketPDFRequest):
    pdf_buffer = generate_ticket_pdf(data)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=ticket.pdf"
        },
    )