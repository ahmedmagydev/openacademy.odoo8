from openerp import fields , models ,api 


class Partner(models.Model):
    _inherit='res.partner'
    
    
    instructor= fields.Boolean("Instructor",default=False)
    session_ids=fields.Many2many('openacademy.session', string='Atendee session', readonly=True)
    