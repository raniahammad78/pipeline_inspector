from odoo import models, fields, api
from odoo.exceptions import ValidationError


# --- INSPECTION MODEL ---
class PipelineInspection(models.Model):
    _name = 'pipeline.inspector.inspection'
    _description = 'Support Inspection'
    _order = 'inspection_date desc'
    _rec_name = 'support_id'

    # UPDATED: Added ondelete='cascade' to fix the deletion error
    support_id = fields.Many2one('pipeline.inspector.support', string="Support", required=True, ondelete='cascade')

    inspector_id = fields.Many2one('res.users', string="Inspector", default=lambda self: self.env.user)
    inspection_date = fields.Datetime(string="Inspection Date", default=fields.Datetime.now)

    state = fields.Selection([
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('issue', 'Issue Found')
    ], string="Status", default='pending')

    # --- THE 9 QUESTIONS ---
    condition_selection = [('c', 'C - Satisfactory'), ('b', 'B - Less Significant'), ('a1', 'A1 - Significant'),
                           ('a2', 'A2 - Imminent')]

    # Q1
    q1_condition = fields.Selection(condition_selection, string="Condition")
    q1_comment = fields.Text(string="Comments")
    q1_recommendation = fields.Text(string="Recommendation")
    q1_images = fields.Many2many('ir.attachment', relation="insp_q1_rel", string="Photos")

    # Q2
    q2_condition = fields.Selection(condition_selection, string="Condition")
    q2_comment = fields.Text(string="Comments")
    q2_recommendation = fields.Text(string="Recommendation")
    q2_images = fields.Many2many('ir.attachment', relation="insp_q2_rel", string="Photos")

    # Q3
    q3_condition = fields.Selection(condition_selection, string="Condition")
    q3_comment = fields.Text(string="Comments")
    q3_recommendation = fields.Text(string="Recommendation")
    q3_images = fields.Many2many('ir.attachment', relation="insp_q3_rel", string="Photos")

    # Q4
    q4_condition = fields.Selection(condition_selection, string="Condition")
    q4_comment = fields.Text(string="Comments")
    q4_recommendation = fields.Text(string="Recommendation")
    q4_images = fields.Many2many('ir.attachment', relation="insp_q4_rel", string="Photos")

    # Q5
    q5_condition = fields.Selection(condition_selection, string="Condition")
    q5_comment = fields.Text(string="Comments")
    q5_recommendation = fields.Text(string="Recommendation")
    q5_images = fields.Many2many('ir.attachment', relation="insp_q5_rel", string="Photos")

    # Q6
    q6_condition = fields.Selection(condition_selection, string="Condition")
    q6_comment = fields.Text(string="Comments")
    q6_recommendation = fields.Text(string="Recommendation")
    q6_images = fields.Many2many('ir.attachment', relation="insp_q6_rel", string="Photos")

    # Q7
    q7_condition = fields.Selection(condition_selection, string="Condition")
    q7_comment = fields.Text(string="Comments")
    q7_recommendation = fields.Text(string="Recommendation")
    q7_images = fields.Many2many('ir.attachment', relation="insp_q7_rel", string="Photos")

    # Q8
    q8_condition = fields.Selection(condition_selection, string="Condition")
    q8_comment = fields.Text(string="Comments")
    q8_recommendation = fields.Text(string="Recommendation")
    q8_images = fields.Many2many('ir.attachment', relation="insp_q8_rel", string="Photos")

    # Q9
    q9_condition = fields.Selection(condition_selection, string="Condition")
    q9_comment = fields.Text(string="Comments")
    q9_recommendation = fields.Text(string="Recommendation")
    q9_images = fields.Many2many('ir.attachment', relation="insp_q9_rel", string="Photos")

    # --- VALIDATION CONSTRAINT ---
    @api.constrains('q1_condition', 'q2_condition', 'q3_condition', 'q4_condition')
    def _check_mandatory_questions(self):
        for record in self:
            if not all([record.q1_condition, record.q2_condition, record.q3_condition, record.q4_condition]):
                raise ValidationError(
                    "Validation Error: You must answer at least the first 4 questions (Q1 - Q4) to save this inspection.")


# --- SUPPORT MODEL ---
class PipelineSupport(models.Model):
    _name = 'pipeline.inspector.support'
    _description = 'Pipeline Structural Support'

    name = fields.Char(string="Full Name", compute="_compute_name", store=True)

    # Fields for the "Add Support" popup
    support_code = fields.Char(string="Support Name", required=True)
    support_level = fields.Char(string="Level")
    pipe_ref = fields.Char(string="Pipe")

    # --- UPDATED CUP TYPE SELECTION (Matches Video) ---
    cup_type = fields.Selection([
        ('u', 'U'),
        ('g', 'G'),
        ('a', 'A'),
        ('r', 'R'),
        ('s', 'S'),
        ('sp', 'SP'),
        ('c', 'C'),
        ('ss', 'SS'),
        ('vudlr', 'VUDLR'),
        ('vddlr', 'VDDLR'),
        ('vudlw', 'VUDLW'),
        ('vddlw', 'VDDLW'),
        ('hdlr', 'HDLR'),
        ('hdlw', 'HDLW'),
        ('fsd', 'FSD'),
        ('hsd', 'HSD'),
        ('fwsd', 'FWSD'),
        ('fcr', 'FCR'),
        ('hcr', 'HCR'),
    ], string="Cup Type")

    # UPDATED: Added ondelete='cascade' here too (Good practice for Pipeline deletion)
    pipeline_id = fields.Many2one('pipeline.inspector.pipeline', string="Pipeline", ondelete='cascade')

    area_type = fields.Char(string="Area Type", default="N/A")

    inspection_ids = fields.One2many('pipeline.inspector.inspection', 'support_id', string="Inspections")

    # Computed fields for the Kanban card
    last_inspection_id = fields.Many2one('pipeline.inspector.inspection', compute='_compute_last_inspection')
    state = fields.Selection(related='last_inspection_id.state', string="Current Status")

    # --- REPORT COMPATIBILITY FIELDS ---
    question_tag = fields.Char(string="Report Condition", compute="_compute_report_data")
    visual_comment = fields.Text(string="Report Comment", compute="_compute_report_data")
    visual_recommendation = fields.Text(string="Report Recommendation", compute="_compute_report_data")
    visual_image = fields.Image(string="Report Image", compute="_compute_report_data")
    visual_caption = fields.Char(string="Report Caption", compute="_compute_report_data")

    @api.depends('support_code', 'support_level', 'pipe_ref')
    def _compute_name(self):
        for record in self:
            parts = [p for p in [record.support_code, record.support_level, record.pipe_ref] if p]
            record.name = " / ".join(parts) if parts else "New Support"

    @api.depends('inspection_ids')
    def _compute_last_inspection(self):
        for record in self:
            record.last_inspection_id = record.inspection_ids[:1]

    @api.depends('last_inspection_id', 'last_inspection_id.q1_condition', 'last_inspection_id.q1_comment',
                 'last_inspection_id.q1_images', 'last_inspection_id.q1_recommendation')
    def _compute_report_data(self):
        for record in self:
            insp = record.last_inspection_id
            if insp:
                record.question_tag = insp.q1_condition.upper() if insp.q1_condition else ''
                record.visual_comment = insp.q1_comment or ''
                record.visual_recommendation = insp.q1_recommendation or ''
                record.visual_caption = 'General Visual'
                if insp.q1_images:
                    record.visual_image = insp.q1_images[0].datas
                else:
                    record.visual_image = False
            else:
                record.question_tag = ''
                record.visual_comment = ''
                record.visual_recommendation = ''
                record.visual_caption = ''
                record.visual_image = False

    def action_edit_last_inspection(self):
        inspection = self.last_inspection_id
        if inspection:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Edit Pipeline Inspection',
                'res_model': 'pipeline.inspector.inspection',
                'res_id': inspection.id,
                'view_mode': 'form',
                'target': 'new',
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'New Pipeline Inspection',
                'res_model': 'pipeline.inspector.inspection',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_support_id': self.id}
            }

    def action_view_inspection(self):
        inspection = self.last_inspection_id
        if not inspection:
            return
        view_id = self.env.ref('pipeline_inspector.pipeline_inspection_report_view').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Inspection Report',
            'res_model': 'pipeline.inspector.inspection',
            'res_id': inspection.id,
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
        }

    def action_save_and_open(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pipeline.inspector.support',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_add_inspection(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Inspection',
            'res_model': 'pipeline.inspector.inspection',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_support_id': self.id}
        }


# --- PIPELINE MODEL ---
class Pipeline(models.Model):
    _name = 'pipeline.inspector.pipeline'
    _description = 'Pipeline'
    _rec_name = 'pipeline_name'

    pipeline_name = fields.Char(string='Pipeline Name', required=True)
    location = fields.Char(string='Location')
    engineer_id = fields.Many2one('res.users', string='Assigned Engineer', default=lambda self: self.env.user)
    state = fields.Selection(
        [('draft', 'Pending'), ('in_progress', 'In Progress'), ('done', 'Done'), ('cancel', 'Cancelled')],
        string='Status', default='draft')

    supports_count = fields.Integer(string='Supports', compute='_compute_counts')
    inspections_count = fields.Integer(string='Inspections', compute='_compute_counts')
    support_ids = fields.One2many('pipeline.inspector.support', 'pipeline_id', string="Supports")

    # --- CHANGED TO CHAR FIELDS (Free Text) ---
    area = fields.Char(string='Area')
    system_name = fields.Char(string='System Name')
    # ------------------------------------------

    drawing_iso_number = fields.Char(string='Drawing ISO Number')
    design_pressure_bar_min = fields.Float(string='Min Pressure')
    design_pressure_bar_max = fields.Float(string='Max Pressure')
    design_temp_c_min = fields.Float(string='Min Temp')
    design_temp_c_max = fields.Float(string='Max Temp')

    # Report Fields
    content_material = fields.Char(string='Content')
    material_grade = fields.Char(string='Material Grade')
    material_lining = fields.Char(string='Material Lining')
    diameter = fields.Char(string='Diameter (in)')
    pipe_schedule = fields.Char(string='Pipe Schedule')
    pipe_thickness = fields.Float(string='Thickness (mm)')

    insulation = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Insulation')
    design_code = fields.Char(string='Design Code')
    corr_allowance = fields.Float(string='Corr. Allowance (mm)')
    operation_pressure = fields.Float(string='Op. Pressure')
    operation_temp = fields.Float(string='Op. Temp')
    painting = fields.Char(string='Painting')
    image_ids = fields.Many2many('ir.attachment', string="Upload Images")

    @api.depends('support_ids', 'support_ids.inspection_ids')
    def _compute_counts(self):
        for record in self:
            record.supports_count = len(record.support_ids)
            all_inspections = record.support_ids.mapped('inspection_ids')
            record.inspections_count = len(all_inspections)

    def action_set_in_progress(self): self.write({'state': 'in_progress'})

    def action_set_done(self): self.write({'state': 'done'})

    def action_reset_draft(self): self.write({'state': 'draft'})

    def action_add_support(self):
        view_id = self.env.ref('pipeline_inspector.view_pipeline_support_create_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add New Support',
            'res_model': 'pipeline.inspector.support',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
            'context': {'default_pipeline_id': self.id}
        }

    def action_delete_pipeline(self):
        self.unlink()
        return {'type': 'ir.actions.act_window_close'}

    def action_print_report(self):
        return self.env.ref('pipeline_inspector.action_report_pipeline').report_action(self)

    def action_open_form(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pipeline.inspector.pipeline',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_edit_support(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pipeline.inspector.support',
            'res_id': self.env.context.get('active_id'),
            'view_mode': 'form',
            'target': 'current',
        }
