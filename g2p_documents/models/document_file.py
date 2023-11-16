import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class G2PDocumentFile(models.Model):
    _inherit = "storage.file"

    tags_ids = fields.Many2many("g2p.document.tag")

    file_type = fields.Char(compute="_compute_file_type")

    def filter_for_tags(self, tags):
        if tags and not isinstance(tags, list):
            tags = [
                tags,
            ]
        return self.filtered(
            lambda x: all((x.tags_ids and tag in x.tags_ids.name) for tag in tags)
        )

    def filter_for_tags_any(self, tags):
        if tags and not isinstance(tags, list):
            tags = [
                tags,
            ]
        return self.filtered(
            lambda x: any((x.tags_ids and tag in x.tags_ids.name) for tag in tags)
        )

    def _compute_file_type(self):
        for file in self:
            if file.extension and isinstance(file.mimetype, str):
                file.file_type = file.mimetype.split("/")[1].upper()
            else:
                file.file_type = False

    def _compute_data(self):
        # Handled key error
        for rec in self:
            try:
                if self._context.get("bin_size"):
                    rec.data = rec.file_size
                elif rec.relative_path:
                    rec.data = rec.backend_id.sudo().get(
                        rec.relative_path, binary=False
                    )
                else:
                    rec.data = None
            except Exception as e:
                # Handle exceptions appropriately
                rec.data = None
                error_message = f"Error computing data for record {rec.id}: {e}"
                _logger.error(error_message)
