from odoo import fields, models


class G2PDocumentFile(models.Model):
    _inherit = "storage.file"

    tags_ids = fields.Many2many("g2p.document.tag")

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
