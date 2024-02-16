from django.db import models

# Create your models here.
class Brands(models.Model):
    BrandID = models.AutoField(primary_key=True)
    BrandName = models.CharField(max_length=225, null=True, blank=True)

    class Meta:
        db_table = "Brands"
    
    def __str__(self):
        return f"BrandID: {self.BrandID}, Brand: {self.BrandName}"

class Categories(models.Model):
    CategoryID = models.AutoField(primary_key=True)
    CategoryName = models.CharField(max_length=225)
    ParentCategoryID = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='child_categories'
    )

    class Meta:
        db_table = "Categories"
    
    def __str__(self):
        return f"Category ID: {self.CategoryID}, Name: {self.CategoryName}, Parent ID: {self.ParentCategoryID}"

class Retailers(models.Model):
    RetailID = models.AutoField(primary_key=True)
    Retail = models.CharField(max_length=225)
    RetailLogo = models.CharField(max_length=225)

    class Meta:
        db_table = "Retailers"
    
    def __str__(self):
        return f"RetailID: {self.RetailID}, Retail: {self.Retail}, RetailLogo: {self.RetailLogo}"

class Products(models.Model):
    ProductID = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=255)
    BrandID = models.ForeignKey(Brands, on_delete=models.CASCADE)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Stock = models.CharField(max_length=25, null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    URL = models.CharField(max_length=500)
    PicURL = models.CharField(max_length=500)
    CategoryID = models.ForeignKey(Categories, on_delete=models.CASCADE)
    RetailID = models.ForeignKey(Retailers, on_delete=models.CASCADE)
    DateEdit = models.DateTimeField(auto_now=True)
    SimilarGroup = models.IntegerField(null=True, blank=True)
    DateCreate = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "Products"
    
    def __str__(self):
        return f"ProductID: {self.ProductID}, ProductName: {self.ProductName}"
    
class Logs(models.Model):
    LogID = models.AutoField(primary_key=True)
    ProductID = models.ForeignKey(Products, on_delete=models.CASCADE)
    EditBy = models.CharField(max_length=25)
    EditAttrib = models.CharField(max_length=225)
    OldData = models.CharField(max_length=225)
    NewData = models.CharField(max_length=225)
    DateEdit = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Logs"
    
    def __str__(self):
        return f"ProductID: {self.ProductID}, EditAttrib: {self.EditAttrib}, OldData: {self.OldData}, NewData: {self.NewData}"