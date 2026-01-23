import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """
    Scripts run before model is load.
    purpose: Delete old Index (if needed) so odoo can create new constraint
    """
    _logger.warning("🚨 Migration is running")
    model_name = "task.task"

    table_name = model_name.replace(".", "_")
    index_name_to_remove = "name_projet_id_unique"

    _logger.info(f"--- [Migration] Cleaning up {table_name} ---")
    cr.execute(f"DROP INDEX IF EXISTS {index_name_to_remove}")
    cr.execute(
        f"ALTER TABLE {table_name} DROP CONSTRAINT IF EXISTS {index_name_to_remove}"
    )
