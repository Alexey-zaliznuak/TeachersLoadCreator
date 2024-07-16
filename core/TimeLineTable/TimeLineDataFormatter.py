from core.TimeLineTable.TimeLine import CELL_WIDTH
from datetime import datetime, timedelta
from models import Booking

CELL_HEIGHT = 40


class TimeLineDataFormatter():
    def __init__(
        self,
        get_bookings,
        get_places,
        select_day=datetime.now()
    ) -> list:

        self.get_bookings = get_bookings
        self.get_places = get_places
        self.places = get_places()

        self.select_day = select_day
        self.select_day = datetime(
            year=self.select_day.year,
            month=self.select_day.month,
            day=self.select_day.day
        )

    def time_to_pixels(self, start_booking_time, end_booking_time):
        tomorrow = self.select_day + timedelta(hours=23, minutes=59)
        start = max(self.select_day, start_booking_time)
        end = min(tomorrow, end_booking_time)

        start = start.hour * CELL_WIDTH + start.minute * CELL_WIDTH / 60
        end = end.hour * CELL_WIDTH + end.minute * CELL_WIDTH / 60 - start

        return {
            'start': start,
            'end': end,
        }

    def get_row(self, bookings):
        books = []
        prev_on_top = False
        for i in range(len(bookings)):
            booking = bookings[i]

            start = booking.start_booking_time
            end = booking.end_booking_time
            height = CELL_HEIGHT if booking.book_full else CELL_HEIGHT / 2

            top = prev_on_top

            if (
                i != 0
                and start < bookings[i - 1].end_booking_time
            ):
                top = not top

            floor = CELL_HEIGHT / 2 if top else 0
            prev_on_top = top
            coordinates = self.time_to_pixels(start, end)

            books.append(
                {
                    'start': coordinates['start'],
                    'end': coordinates['end'],
                    'floor': floor,
                    'height': height,
                }
            )

        return books

    def get_rows(self):
        rows = []
        self.places = self.get_places()

        for place in self.places:
            books = self.get_bookings().where(
                Booking.place == place,
                Booking.start_booking_time <= datetime(
                    year=self.select_day.year,
                    month=self.select_day.month,
                    day=self.select_day.day
                ) + timedelta(days=1) - timedelta(microseconds=1),
                Booking.end_booking_time >= datetime(
                    year=self.select_day.year,
                    month=self.select_day.month,
                    day=self.select_day.day
                )
            )
            books = sorted(books, key=lambda x: x.start_booking_time)
            rows.append(
                {
                    'data': [*self.get_row(books)],
                    'name': place.name
                }
            )
        return rows
