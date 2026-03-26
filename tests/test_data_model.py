import pytest
from Whatsapp_Chat_Exporter.data_model import TimeZone, Timing
from datetime import timedelta


class TestTimeZone:
    def test_utcoffset(self):
        tz = TimeZone(5.5)
        assert tz.utcoffset(None) == timedelta(hours=5.5)

    def test_dst(self):
        tz = TimeZone(2)
        assert tz.dst(None) == timedelta(0)


class TestTiming:   
    @pytest.mark.parametrize("offset, expected_hour", [
        (8, "08:00"),      # Integer (e.g., Hong Kong Standard Time)
        (-8, "16:00"),     # Negative Integer (e.g., PST)
        (5.5, "05:30"),    # Positive Float (e.g., IST)
        (-3.5, "20:30"),   # Negative Float (e.g., Newfoundland)
    ])

    def test_format_timestamp_various_offsets(self, offset, expected_hour):
        """Verify that both int and float offsets calculate time correctly."""
        t = Timing(offset)
        result = t.format_timestamp(1672531200, "%H:%M")
        assert result == expected_hour

    @pytest.mark.parametrize("ts_input", [
        1672531200,        # Unix timestamp as int
        1672531200.0,      # Unix timestamp as float
    ])

    def test_timestamp_input_types(self, ts_input):
        """Verify the method accepts both int and float timestamps."""
        t = Timing(0)
        result = t.format_timestamp(ts_input, "%Y")
        assert result == "2023"

    def test_timing_none_offset(self):
        """Verify initialization with None doesn't crash and uses system time."""
        t = Timing(None)
        assert t.tz is None
        # Should still return a valid string based on local machine time without crashing
        result = t.format_timestamp(1672531200, "%Y")
        assert result == "2023"

    def test_millisecond_scaling(self):
        """Verify that timestamps in milliseconds are correctly scaled down."""
        t = Timing(0)
        # Milliseconds as int
        assert t.format_timestamp(1672531200000, "%Y") == "2023"
        # Milliseconds as float
        assert t.format_timestamp(1672531200000.0, "%Y") == "2023"
