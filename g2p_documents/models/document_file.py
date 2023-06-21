from odoo import fields, models


class G2PDocumentFile(models.Model):
    _inherit = "storage.file"

    tags_ids = fields.Many2many("g2p.document.tag")

    def filter_for_tags(self, tags):
        if tags and not isinstance(tags, list):
            tags = [
                tags,
            ]
        return self.filtered(lambda x: all(tag in x.tags_ids.name for tag in tags))
