from odoo import models, fields, api
from datetime import date


class PipelineDashboard(models.Model):
    _name = 'pipeline.inspector.dashboard'
    _description = 'Pipeline Inspector Dashboard'

    name = fields.Char(string="Name", default="Main Dashboard")

    filter_option = fields.Selection([
        ('all', 'All Time'),
        ('month', 'This Month'),
        ('today', 'Today')
    ], string="Time Filter", default='all', required=True)

    # Metrics
    total_pipelines = fields.Integer(compute='_compute_dashboard_data')
    active_inspections = fields.Integer(compute='_compute_dashboard_data')
    engineers_count = fields.Integer(compute='_compute_dashboard_data')

    # Progress
    percent_done = fields.Float(compute='_compute_dashboard_data')
    percent_in_progress = fields.Float(compute='_compute_dashboard_data')
    percent_pending = fields.Float(compute='_compute_dashboard_data')

    # Recent List
    recent_pipeline_ids = fields.Many2many(
        'pipeline.inspector.pipeline',
        compute='_compute_dashboard_data'
    )

    # --- Actions for the Right-Aligned Buttons ---
    def set_filter_all(self):
        self.write({'filter_option': 'all'})
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def set_filter_month(self):
        self.write({'filter_option': 'month'})
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def set_filter_today(self):
        self.write({'filter_option': 'today'})
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    @api.depends('filter_option')
    def _compute_dashboard_data(self):
        for record in self:
            domain = []
            if record.filter_option == 'month':
                today = date.today()
                start_date = today.replace(day=1)
                domain = [('create_date', '>=', start_date)]
            elif record.filter_option == 'today':
                domain = [('create_date', '>=', date.today())]

            filtered_pipelines = self.env['pipeline.inspector.pipeline'].search(domain)
            total = len(filtered_pipelines)

            record.total_pipelines = total
            record.active_inspections = len(filtered_pipelines.filtered(lambda p: p.state in ['in_progress', 'draft']))
            record.engineers_count = len(filtered_pipelines.mapped('engineer_id'))

            if total > 0:
                record.percent_done = (len(filtered_pipelines.filtered(lambda p: p.state == 'done')) / total) * 100
                record.percent_in_progress = (len(filtered_pipelines.filtered(
                    lambda p: p.state == 'in_progress')) / total) * 100
                record.percent_pending = (len(filtered_pipelines.filtered(lambda p: p.state == 'draft')) / total) * 100
            else:
                record.percent_done = record.percent_in_progress = record.percent_pending = 0

            record.recent_pipeline_ids = self.env['pipeline.inspector.pipeline'].search(domain, order='id desc',
                                                                                        limit=5)

    def action_create_new_pipeline(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Pipeline',
            'res_model': 'pipeline.inspector.pipeline',
            'view_mode': 'form',
            'target': 'current',
        }
