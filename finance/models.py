from django.db import models
from students.models import Student
from staff.models import Staff
from django.utils import timezone

class FeeItem(models.Model):
    name = models.CharField(max_length=100) # e.g., "Grade 10 Tuition"
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} (AED{self.amount})"

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='invoices')
    fee_item = models.ForeignKey(FeeItem, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Snapshot of cost
    date_issued = models.DateField(default=timezone.now)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')

    def __str__(self):
        return f"Inv #{self.id} - {self.student} - {self.status}"

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(default=timezone.now)
    remarks = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Payment of AED{self.amount_paid} for Inv #{self.invoice.id}"
    
class SalarySlip(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    month = models.DateField(help_text="The 1st of the month this salary is for")
    
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Bonuses, Transport, etc.")
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Tax, Loans, etc.")
    
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ['staff', 'month'] # Prevent paying someone twice in the same month

    def save(self, *args, **kwargs):
        # Auto-calculate Net Salary
        self.net_salary = float(self.basic_salary) + float(self.allowances) - float(self.deductions)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.staff.first_name} - {self.month.strftime('%B %Y')}"