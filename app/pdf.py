from io import BytesIO

import qrcode

from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def draw_text_fit(
    pdf,
    text,
    x,
    y,
    max_width,
    font_name="Helvetica-Bold",
    max_font_size=16,
    min_font_size=7,
    color=colors.black,
):
    """
    Малює текст із автоматичним зменшенням шрифту,
    якщо текст не поміщається у задану ширину.
    """

    text = str(text)

    font_size = max_font_size

    while (
        font_size > min_font_size
        and pdf.stringWidth(text, font_name, font_size) > max_width
    ):
        font_size -= 1

    pdf.setFillColor(color)
    pdf.setFont(font_name, font_size)

    pdf.drawString(
        x,
        y,
        text,
    )


def generate_ticket_pdf(data) -> BytesIO:
    # ---------------------------------------------------------
    # Boarding pass
    # ---------------------------------------------------------

    width = 756
    height = 303

    buffer = BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=(width, height),
    )

    # ---------------------------------------------------------
    # Colors
    # ---------------------------------------------------------

    purple = colors.HexColor("#7B2CBF")
    dark = colors.HexColor("#222222")
    gray = colors.HexColor("#555555")
    light_gray = colors.HexColor("#CCCCCC")

    # ---------------------------------------------------------
    # Data
    # ---------------------------------------------------------

    departure_country = data.departure_country
    arrival_country = data.arrival_country

    departure_airport = data.departure_airport
    arrival_airport = data.arrival_airport

    passenger_name = data.passenger_name
    flight_number = data.flight_number
    seat_number = data.seat_number
    airline = data.airline

    # ---------------------------------------------------------
    # Background
    # ---------------------------------------------------------

    pdf.setFillColor(colors.white)

    pdf.roundRect(
        10,
        10,
        width - 20,
        height - 20,
        15,
        fill=1,
        stroke=0,
    )

    # ---------------------------------------------------------
    # Upper purple part
    # ---------------------------------------------------------

    pdf.setFillColor(purple)

    pdf.roundRect(
        10,
        height - 65,
        width - 20,
        55,
        15,
        fill=1,
        stroke=0,
    )

    # Close the bottom part of the curve

    pdf.rect(
        10,
        height - 65,
        width - 20,
        20,
        fill=1,
        stroke=0,
    )

    # ---------------------------------------------------------
    # Title
    # ---------------------------------------------------------

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawString(
        35,
        height - 45,
        "AIRLINE TICKET",
    )

    pdf.drawCentredString(
        width / 2,
        height - 45,
        "BOARDING PASS",
    )

    # ---------------------------------------------------------
    # Vertical line before the tear-off section
    # ---------------------------------------------------------

    separator_x = 570

    pdf.setStrokeColor(light_gray)
    pdf.setDash(4, 4)

    pdf.line(
        separator_x,
        20,
        separator_x,
        height - 15,
    )

    pdf.setDash()

    # ---------------------------------------------------------
    # FROM
    # ---------------------------------------------------------

    pdf.setFillColor(gray)
    pdf.setFont("Helvetica-Bold", 9)

    pdf.drawString(
        45,
        215,
        "FROM:",
    )

    # Country
    draw_text_fit(
        pdf,
        departure_country,
        x=45,
        y=165,
        max_width=190,
        max_font_size=38,
        min_font_size=16,
        color=purple,
    )

    # Airport
    draw_text_fit(
        pdf,
        departure_airport.upper(),
        x=45,
        y=145,
        max_width=190,
        max_font_size=16,
        min_font_size=8,
        color=dark,
    )

    # ---------------------------------------------------------
    # TO
    # ---------------------------------------------------------

    pdf.setFillColor(gray)
    pdf.setFont("Helvetica-Bold", 9)

    pdf.drawString(
        300,
        215,
        "TO:",
    )

    # Country
    draw_text_fit(
        pdf,
        arrival_country,
        x=300,
        y=165,
        max_width=140,
        max_font_size=38,
        min_font_size=16,
        color=purple,
    )

    # Airport
    draw_text_fit(
        pdf,
        arrival_airport.upper(),
        x=300,
        y=145,
        max_width=140,
        max_font_size=16,
        min_font_size=8,
        color=dark,
    )

    # ---------------------------------------------------------
    # Airplane between cities
    # ---------------------------------------------------------

    pdf.setFillColor(purple)
    pdf.setFont("Helvetica-Bold", 28)

    pdf.drawCentredString(
        250,
        170,
        "✈",
    )

    # ---------------------------------------------------------
    # Data / time
    # ---------------------------------------------------------

    pdf.setFillColor(dark)
    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        45,
        125,
        data.departure_time.strftime("%b %d, %Y"),
    )

    pdf.drawString(
        45,
        110,
        data.departure_time.strftime("%H:%M"),
    )

    pdf.drawString(
        300,
        125,
        data.arrival_time.strftime("%b %d, %Y"),
    )

    pdf.drawString(
        300,
        110,
        data.arrival_time.strftime("%H:%M"),
    )

    # ---------------------------------------------------------
    # PASSENGER DATA
    # ---------------------------------------------------------

    y_label = 75
    y_value = 55

    columns = [
        (
            "PASSENGER NAME",
            passenger_name,
            45,
            190,
        ),
        (
            "FLIGHT",
            flight_number,
            250,
            80,
        ),
        (
            "SEAT",
            seat_number,
            345,
            50,
        ),
        (
            "AIRLINE",
            airline,
            410,
            140,
        ),
    ]

    for label, value, x, max_width in columns:

        pdf.setFillColor(gray)
        pdf.setFont("Helvetica-Bold", 7)

        pdf.drawString(
            x,
            y_label,
            label,
        )

        draw_text_fit(
            pdf,
            value,
            x=x,
            y=y_value,
            max_width=max_width,
            font_name="Helvetica-Bold",
            max_font_size=11,
            min_font_size=6,
            color=dark,
        )

    # ---------------------------------------------------------
    # QR CODE
    # ---------------------------------------------------------

    qr_data = (
        f"ticket:{data.ticket_id};"
        f"flight:{flight_number};"
        f"seat:{seat_number}"
    )

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=6,
        border=2,
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    qr_image = qr.make_image(
        fill_color="black",
        back_color="white",
    )

    qr_buffer = BytesIO()

    qr_image.save(
        qr_buffer,
        format="PNG",
    )

    qr_buffer.seek(0)

    qr_reader = ImageReader(qr_buffer)

    # ---------------------------------------------------------
    # Main QR
    # ---------------------------------------------------------

    pdf.drawImage(
        qr_reader,
        455,
        110,
        width=90,
        height=90,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )

    # ---------------------------------------------------------
    # Tear-off section
    # ---------------------------------------------------------

    pdf.setFillColor(gray)
    pdf.setFont("Helvetica-Bold", 7)

    pdf.drawString(
        590,
        215,
        "FROM",
    )

    pdf.drawString(
        590,
        155,
        "TO",
    )

    # ---------------------------------------------------------
    # Departure country
    # ---------------------------------------------------------

    draw_text_fit(
        pdf,
        departure_country,
        x=590,
        y=180,
        max_width=65,
        max_font_size=24,
        min_font_size=8,
        color=purple,
    )

    # ---------------------------------------------------------
    # Arrival country
    # ---------------------------------------------------------

    draw_text_fit(
        pdf,
        arrival_country,
        x=590,
        y=125,
        max_width=65,
        max_font_size=24,
        min_font_size=8,
        color=purple,
    )

    # ---------------------------------------------------------
    # Passenger
    # ---------------------------------------------------------

    pdf.setFillColor(gray)
    pdf.setFont("Helvetica-Bold", 7)

    pdf.drawString(
        590,
        85,
        "PASSENGER NAME",
    )

    draw_text_fit(
        pdf,
        passenger_name,
        x=590,
        y=70,
        max_width=105,
        font_name="Helvetica-Bold",
        max_font_size=10,
        min_font_size=6,
        color=dark,
    )

    # ---------------------------------------------------------
    # Seat / Airline
    # ---------------------------------------------------------

    small_data = [
        (
            "SEAT",
            seat_number,
            590,
            45,
        ),
        (
            "AIRLINE",
            airline,
            650,
            45,
        ),
    ]

    for label, value, x, max_width in small_data:

        pdf.setFillColor(gray)
        pdf.setFont("Helvetica-Bold", 6)

        pdf.drawString(
            x,
            45,
            label,
        )

        draw_text_fit(
            pdf,
            value,
            x=x,
            y=30,
            max_width=max_width,
            font_name="Helvetica-Bold",
            max_font_size=9,
            min_font_size=5,
            color=dark,
        )

    # ---------------------------------------------------------
    # QR code on the tear-off section
    # ---------------------------------------------------------

    pdf.drawImage(
        qr_reader,
        700,
        25,
        width=45,
        height=45,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )

    # ---------------------------------------------------------
    # End PDF
    # ---------------------------------------------------------

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    return buffer