from logging import getLogger

from core.models import Record


logger = getLogger(__name__)


def get_data_all() -> list[Record]:
    """
    Fetching all data from Records.

    """
    data = Record.objects.all()
    logger.info('Got all records.')
    return list(data)
