from openerp import fields , api , models ,exceptions


class Course(models.Model):

  _name='openacademy.course'
  
  
  
  name = fields.Char(string="Title", required=True)
  description = fields.Text()
  responsible_id = fields.Many2one('res.users',ondelete='set null', string="Responsible", index=True)
  session_ids=fields.One2many('openacademy.session','course_id',string='Session')
  
  
  
  
  
  _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]
  
  

class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    active=fields.Boolean(defualt=True)
    
    instructor_id = fields.Many2one('res.partner', string="Instructor",
    domain=['|',('instructor','=',True),('category_id.name','ilike','Teacher')]
    )
    course_id = fields.Many2one('openacademy.course',ondelete='cascade', string="Course", required=True)
    attendee_ids= fields.Many2many('res.partner', string='Attendees')
    
    
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    state= fields.Selection([('draft',"Draft"),
                             ('confirmed','Confirmed'),
                             ('done','Done'),
                             ], default='draft')
  
  
  
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats
                
                
                
                
    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }
            
            
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")
    
    
    
    
    @api.multi
    def action_draft(self):
      self.state = 'draft'
      
    @api.multi
    def action_confirmed(self):
      self.state = 'confirmed'
      
    @api.multi
    def action_done(self):
      self.state = 'done'
      
    
            