from django.core.management.base import BaseCommand
from gestion_paie.models import TypeElement, ParametrePaie
from datetime import date

class Command(BaseCommand):
    help = 'Initialise les données de base pour la gestion de paie'

    def handle(self, *args, **kwargs):
        self.stdout.write('Création des types d\'éléments de paie...')
        
        # Primes
        primes = [
            ('PRIME_TRANS', 'Prime de transport', 'prime', 'Indemnité de transport'),
            ('PRIME_LOG', 'Prime de logement', 'prime', 'Indemnité de logement'),
            ('PRIME_PERF', 'Prime de performance', 'prime', 'Prime basée sur les performances'),
            ('PRIME_ANC', 'Prime d\'ancienneté', 'prime', 'Prime liée à l\'ancienneté'),
            ('PRIME_RESP', 'Prime de responsabilité', 'prime', 'Prime pour poste à responsabilité'),
            ('PRIME_TECH', 'Prime technique', 'prime', 'Prime pour compétences techniques'),
        ]
        
        for code, nom, type_el, desc in primes:
            TypeElement.objects.get_or_create(
                code=code,
                defaults={
                    'nom': nom,
                    'type_element': type_el,
                    'description': desc,
                    'actif': True
                }
            )
            self.stdout.write(self.style.SUCCESS(f'✓ {nom}'))
        
        # Déductions
        deductions = [
            ('DED_AVANCE', 'Avance sur salaire', 'deduction', 'Remboursement d\'avance'),
            ('DED_PRET', 'Remboursement prêt', 'deduction', 'Remboursement de prêt'),
            ('DED_RETARD', 'Retenue pour retard', 'deduction', 'Pénalité pour retards'),
            ('DED_ABSENCE', 'Retenue pour absence', 'deduction', 'Déduction pour absences injustifiées'),
            ('DED_AUTRE', 'Autre déduction', 'deduction', 'Autre type de déduction'),
        ]
        
        for code, nom, type_el, desc in deductions:
            TypeElement.objects.get_or_create(
                code=code,
                defaults={
                    'nom': nom,
                    'type_element': type_el,
                    'description': desc,
                    'actif': True
                }
            )
            self.stdout.write(self.style.SUCCESS(f'✓ {nom}'))
        
        # Paramètres de paie
        self.stdout.write('\nCréation des paramètres de paie...')
        
        ParametrePaie.objects.get_or_create(
            date_application=date(2024, 1, 1),
            defaults={
                'taux_cotisation_employe': 5.00,
                'taux_cotisation_employeur': 16.00,
                'taux_heure_sup_normale': 125.00,
                'taux_heure_sup_nuit': 150.00,
                'taux_heure_sup_weekend': 175.00,
                'tranche1_max': 30000,
                'tranche1_taux': 0,
                'tranche2_max': 50000,
                'tranche2_taux': 10,
                'tranche3_max': 80000,
                'tranche3_taux': 15,
                'tranche4_max': 120000,
                'tranche4_taux': 20,
                'tranche5_taux': 25,
                'heures_travail_mensuel': 173,
                'actif': True
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ Paramètres de paie créés'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Initialisation terminée avec succès!'))