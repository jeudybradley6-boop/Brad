from django.db import models
from django.contrib.auth.models import User

# Modèl Product
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

# Modèl Commande (Kòmand) ak Many-to-Many
class Commande(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produits = models.ManyToManyField(Product, through='CommandeItem', blank=True)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_commande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.prix_total} HT"

    # Fonksyon pou mete pri total otomatik
    def calculer_prix_total(self):
        total = sum([item.prix_total for item in self.commandeitem_set.all()])
        self.prix_total = total
        self.save()

# Modèl intermediary pou Many-to-Many ak kantite pou chak pwodwi
class CommandeItem(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.prix_total = self.produit.price * self.quantite
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantite} x {self.produit.name}"

# Modèl CartItem (pou pannye)
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.produit.name} pour {self.user.username}"