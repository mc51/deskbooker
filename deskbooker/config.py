class Config:
    MAX_DESK_BOOKING_DAYS = (
        12  # How many days in advance can we book (set my deskbird server)
    )
    MAX_STATUS_BOOKING_DAYS = 30
    DEFAULT_STATUS_BOOKING_DAYS = 7  # for weekly status updates
    WEEKDAY_TO_BOOK = [1, 2]  # Book only for this weekdays, Mo = 0 Sun = 6
