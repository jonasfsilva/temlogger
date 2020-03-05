from collections import OrderedDict

from .base import FormatterBase


class StackDriverFormatter(FormatterBase):

    def format(self, record):
        message = OrderedDict([
            ('@timestamp', self.format_timestamp(record.created)),
            ('message', record.getMessage()),
            ('host', self.host),
            ('path', record.pathname),
            ('environment', self.environment),

            # Extra Fields
            ('level', record.levelname),
            ('logger_name', record.name),
        ])

        # Add extra fields
        message.update(self.get_extra_fields(record))

        # If exception, add debug info
        if record.exc_info:
            message.update(self.get_debug_fields(record))

        return message
