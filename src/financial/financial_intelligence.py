"""
Ascension AI - Financial Intelligence System
Complete financial analysis and wealth building
"""

import torch
import torch.nn as nn
from typing import Dict, List, Optional
import json
import os
from datetime import datetime
from collections import defaultdict

class FinancialAnalyzer:
    """Analyze financial situation"""
    
    def __init__(self):
        self.financial_metrics = {
            'credit_score': 0,
            'income': 0,
            'debt': 0,
            'savings': 0,
            'monthly_expenses': 0
        }
    
    def analyze_financial_health(self, user_id: str, financial_data: Dict) -> Dict:
        """Analyze overall financial health"""
        credit_score = financial_data.get('credit_score', 0)
        monthly_income = financial_data.get('monthly_income', 0)
        total_debt = financial_data.get('total_debt', 0)
        monthly_expenses = financial_data.get('monthly_expenses', 0)
        savings = financial_data.get('savings', 0)
        
        # Calculate ratios
        debt_to_income = total_debt / (monthly_income * 12) if monthly_income > 0 else 0
        expense_to_income = monthly_expenses / monthly_income if monthly_income > 0 else 0
        savings_rate = savings / (monthly_income * 12) if monthly_income > 0 else 0
        
        # Determine health score
        health_score = self.calculate_health_score(credit_score, debt_to_income, expense_to_income, savings_rate)
        
        return {
            'user_id': user_id,
            'health_score': health_score,
            'health_category': self.get_health_category(health_score),
            'credit_score': credit_score,
            'debt_to_income_ratio': debt_to_income,
            'expense_to_income_ratio': expense_to_income,
            'savings_rate': savings_rate,
            'analyzed_at': datetime.now().isoformat()
        }
    
    def calculate_health_score(self, credit_score: int, debt_to_income: float, expense_to_income: float, savings_rate: float) -> float:
        """Calculate overall financial health score"""
        score = 0
        
        # Credit score (30%)
        if credit_score >= 750:
            score += 30
        elif credit_score >= 700:
            score += 25
        elif credit_score >= 650:
            score += 20
        elif credit_score >= 600:
            score += 15
        else:
            score += 10
        
        # Debt to income (25%)
        if debt_to_income <= 0.3:
            score += 25
        elif debt_to_income <= 0.4:
            score += 20
        elif debt_to_income <= 0.5:
            score += 15
        else:
            score += 10
        
        # Expense to income (25%)
        if expense_to_income <= 0.5:
            score += 25
        elif expense_to_income <= 0.7:
            score += 20
        elif expense_to_income <= 0.85:
            score += 15
        else:
            score += 10
        
        # Savings rate (20%)
        if savings_rate >= 0.2:
            score += 20
        elif savings_rate >= 0.1:
            score += 15
        elif savings_rate >= 0.05:
            score += 10
        else:
            score += 5
        
        return score
    
    def get_health_category(self, score: float) -> str:
        """Get health category from score"""
        if score >= 80:
            return 'excellent'
        elif score >= 60:
            return 'good'
        elif score >= 40:
            return 'fair'
        else:
            return 'poor'

class SpendingAnalyzer:
    """Analyze spending habits"""
    
    def __init__(self):
        self.spending_categories = {
            'housing': ['rent', 'mortgage', 'utilities', 'maintenance'],
            'food': ['groceries', 'dining_out', 'coffee'],
            'transportation': ['car_payment', 'gas', 'insurance', 'public_transit'],
            'entertainment': ['streaming', 'movies', 'games', 'hobbies'],
            'shopping': ['clothing', 'electronics', 'home_goods'],
            'health': ['insurance', 'medications', 'gym'],
            'debt_payments': ['credit_card', 'loans'],
            'savings': ['emergency_fund', 'investments']
        }
    
    def analyze_spending(self, user_id: str, spending_data: List[Dict]) -> Dict:
        """Analyze spending patterns"""
        # Categorize spending
        categorized = self.categorize_spending(spending_data)
        
        # Identify patterns
        patterns = self.identify_patterns(categorized)
        
        # Find waste
        waste = self.identify_waste(categorized)
        
        # Generate insights
        insights = self.generate_insights(categorized, patterns, waste)
        
        return {
            'user_id': user_id,
            'categorized_spending': categorized,
            'patterns': patterns,
            'waste': waste,
            'insights': insights,
            'analyzed_at': datetime.now().isoformat()
        }
    
    def categorize_spending(self, spending_data: List[Dict]) -> Dict:
        """Categorize spending data"""
        categorized = defaultdict(float)
        
        for item in spending_data:
            category = self.determine_category(item.get('description', ''))
            amount = item.get('amount', 0)
            categorized[category] += amount
        
        return dict(categorized)
    
    def determine_category(self, description: str) -> str:
        """Determine category from description"""
        description_lower = description.lower()
        
        for category, keywords in self.spending_categories.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return category
        
        return 'other'
    
    def identify_patterns(self, categorized: Dict) -> List[str]:
        """Identify spending patterns"""
        patterns = []
        
        total = sum(categorized.values())
        
        for category, amount in categorized.items():
            percentage = (amount / total) * 100 if total > 0 else 0
            
            if percentage > 30:
                patterns.append(f'High spending in {category}: {percentage:.1f}%')
            elif percentage > 20:
                patterns.append(f'Moderate spending in {category}: {percentage:.1f}%')
        
        return patterns
    
    def identify_waste(self, categorized: Dict) -> List[Dict]:
        """Identify wasteful spending"""
        waste = []
        
        # Entertainment spending > 15% of total
        entertainment = categorized.get('entertainment', 0)
        total = sum(categorized.values())
        
        if total > 0 and (entertainment / total) > 0.15:
            waste.append({
                'category': 'entertainment',
                'amount': entertainment,
                'percentage': (entertainment / total) * 100,
                'suggestion': 'Consider reducing entertainment spending'
            })
        
        # Dining out > 10% of total
        food = categorized.get('food', 0)
        if total > 0 and (food / total) > 0.15:
            waste.append({
                'category': 'food',
                'amount': food,
                'percentage': (food / total) * 100,
                'suggestion': 'Consider cooking at home more often'
            })
        
        return waste
    
    def generate_insights(self, categorized: Dict, patterns: List[str], waste: List[Dict]) -> List[str]:
        """Generate spending insights"""
        insights = []
        
        if waste:
            insights.append(f'Found {len(waste)} areas of potential savings')
        
        total = sum(categorized.values())
        savings = categorized.get('savings', 0)
        
        if total > 0:
            savings_rate = (savings / total) * 100
            if savings_rate < 10:
                insights.append('Savings rate is below recommended 20%')
            elif savings_rate >= 20:
                insights.append('Good savings rate maintained')
        
        return insights

class OpportunityFinder:
    """Find wealth building opportunities"""
    
    def __init__(self):
        self.opportunity_types = {
            'investment': ['stocks', 'bonds', 'real_estate', 'crypto', 'index_funds'],
            'business': ['side_hustle', 'freelance', 'consulting', 'ecommerce'],
            'education': ['certifications', 'skills', 'degrees'],
            'passive': ['dividends', 'rental', 'royalties', 'affiliate']
        }
    
    def find_opportunities(self, user_id: str, user_profile: Dict, financial_data: Dict) -> Dict:
        """Find personalized opportunities"""
        opportunities = []
        
        # Investment opportunities
        if financial_data.get('savings', 0) > 1000:
            opportunities.extend(self.find_investment_opportunities(financial_data))
        
        # Business opportunities
        opportunities.extend(self.find_business_opportunities(user_profile))
        
        # Education opportunities
        opportunities.extend(self.find_education_opportunities(user_profile))
        
        # Passive income opportunities
        opportunities.extend(self.find_passive_opportunities(financial_data))
        
        # Rank opportunities
        ranked = self.rank_opportunities(opportunities, user_profile, financial_data)
        
        return {
            'user_id': user_id,
            'opportunities': ranked,
            'total_opportunities': len(ranked),
            'found_at': datetime.now().isoformat()
        }
    
    def find_investment_opportunities(self, financial_data: Dict) -> List[Dict]:
        """Find investment opportunities"""
        opportunities = []
        savings = financial_data.get('savings', 0)
        
        if savings >= 1000:
            opportunities.append({
                'type': 'investment',
                'category': 'index_funds',
                'title': 'Index Fund Investment',
                'description': 'Low-cost index funds for long-term growth',
                'minimum_investment': 1000,
                'expected_return': '7-10% annually',
                'risk_level': 'moderate',
                'time_horizon': '5+ years'
            })
        
        if savings >= 5000:
            opportunities.append({
                'type': 'investment',
                'category': 'stocks',
                'title': 'Individual Stock Investment',
                'description': 'Build a diversified stock portfolio',
                'minimum_investment': 5000,
                'expected_return': '8-12% annually',
                'risk_level': 'moderate_to_high',
                'time_horizon': '3+ years'
            })
        
        return opportunities
    
    def find_business_opportunities(self, user_profile: Dict) -> List[Dict]:
        """Find business opportunities"""
        opportunities = []
        skills = user_profile.get('skills', [])
        
        # Skill-based opportunities
        skill_mapping = {
            'writing': ['freelance_writing', 'content_creation'],
            'design': ['graphic_design', 'ui_ux'],
            'programming': ['web_development', 'app_development'],
            'teaching': ['tutoring', 'online_courses'],
            'marketing': ['social_media', 'email_marketing']
        }
        
        for skill in skills:
            if skill in skill_mapping:
                for opportunity in skill_mapping[skill]:
                    opportunities.append({
                        'type': 'business',
                        'category': 'side_hustle',
                        'title': f'{opportunity.replace("_", " ").title()}',
                        'description': f'Monetize your {skill} skills',
                        'startup_cost': 0,
                        'expected_income': '$500-2000/month',
                        'time_commitment': '10-20 hours/week',
                        'skill_required': skill
                    })
        
        return opportunities
    
    def find_education_opportunities(self, user_profile: Dict) -> List[Dict]:
        """Find education opportunities"""
        opportunities = []
        
        opportunities.append({
            'type': 'education',
            'category': 'skills',
            'title': 'High-Income Skill Development',
            'description': 'Learn skills that pay $50+/hour',
            'cost': '$0-500',
            'expected_return': '$20,000-100,000/year increase',
            'time_commitment': '3-12 months',
            'examples': ['coding', 'data analysis', 'digital marketing', 'sales']
        })
        
        return opportunities
    
    def find_passive_opportunities(self, financial_data: Dict) -> List[Dict]:
        """Find passive income opportunities"""
        opportunities = []
        
        opportunities.append({
            'type': 'passive',
            'category': 'dividends',
            'title': 'Dividend Investing',
            'description': 'Generate passive income through dividend stocks',
            'minimum_investment': 1000,
            'expected_return': '3-5% annually',
            'risk_level': 'moderate',
            'time_commitment': 'minimal'
        })
        
        return opportunities
    
    def rank_opportunities(self, opportunities: List[Dict], user_profile: Dict, financial_data: Dict) -> List[Dict]:
        """Rank opportunities by suitability"""
        for opp in opportunities:
            opp['suitability_score'] = self.calculate_suitability(opp, user_profile, financial_data)
        
        return sorted(opportunities, key=lambda x: x['suitability_score'], reverse=True)
    
    def calculate_suitability(self, opportunity: Dict, user_profile: Dict, financial_data: Dict) -> float:
        """Calculate suitability score for opportunity"""
        score = 50
        
        # Check financial suitability
        if 'minimum_investment' in opportunity:
            savings = financial_data.get('savings', 0)
            if savings >= opportunity['minimum_investment']:
                score += 30
            else:
                score -= 20
        
        # Check skill suitability
        if 'skill_required' in opportunity:
            skills = user_profile.get('skills', [])
            if opportunity['skill_required'] in skills:
                score += 20
        
        # Check time suitability
        time_available = user_profile.get('available_hours', 10)
        if 'time_commitment' in opportunity:
            if 'minimal' in opportunity['time_commitment'].lower():
                score += 10
            elif time_available >= 10:
                score += 10
        
        return score

class WealthBuilder:
    """Build step-by-step wealth plans"""
    
    def __init__(self):
        self.wealth_stages = {
            'stage_1': {'name': 'Foundation', 'target': 1000, 'focus': 'emergency_fund'},
            'stage_2': {'name': 'Stability', 'target': 10000, 'focus': 'debt_elimination'},
            'stage_3': {'name': 'Growth', 'target': 100000, 'focus': 'investing'},
            'stage_4': {'name': 'Acceleration', 'target': 1000000, 'focus': 'scaling'}
        }
    
    def create_wealth_plan(self, user_id: str, current_savings: int, target: int = 1000000) -> Dict:
        """Create step-by-step wealth building plan"""
        current_stage = self.determine_current_stage(current_savings)
        stages = self.build_stage_sequence(current_stage, target)
        
        return {
            'user_id': user_id,
            'current_savings': current_savings,
            'target': target,
            'current_stage': current_stage,
            'wealth_stages': stages,
            'estimated_time': self.estimate_time_to_target(current_savings, target),
            'created_at': datetime.now().isoformat()
        }
    
    def determine_current_stage(self, savings: int) -> str:
        """Determine current wealth stage"""
        if savings < 1000:
            return 'stage_1'
        elif savings < 10000:
            return 'stage_2'
        elif savings < 100000:
            return 'stage_3'
        else:
            return 'stage_4'
    
    def build_stage_sequence(self, current_stage: str, target: int) -> List[Dict]:
        """Build sequence of wealth stages"""
        stages = []
        stage_order = ['stage_1', 'stage_2', 'stage_3', 'stage_4']
        
        start_index = stage_order.index(current_stage)
        
        for i in range(start_index, len(stage_order)):
            stage_name = stage_order[i]
            stage_info = self.wealth_stages[stage_name]
            
            stage = {
                'stage': stage_name,
                'name': stage_info['name'],
                'target': stage_info['target'],
                'focus': stage_info['focus'],
                'steps': self.generate_stage_steps(stage_name),
                'time_estimate': self.estimate_stage_time(stage_name)
            }
            
            stages.append(stage)
        
        return stages
    
    def generate_stage_steps(self, stage: str) -> List[Dict]:
        """Generate steps for a wealth stage"""
        if stage == 'stage_1':
            return [
                {'step': 1, 'action': 'Build emergency fund', 'target': 1000, 'time': '3-6 months'},
                {'step': 2, 'action': 'Track all spending', 'target': '100% tracking', 'time': '1 month'},
                {'step': 3, 'action': 'Reduce unnecessary expenses', 'target': 'Save 20% of income', 'time': 'ongoing'}
            ]
        elif stage == 'stage_2':
            return [
                {'step': 1, 'action': 'Pay off high-interest debt', 'target': '0 high-interest debt', 'time': '6-12 months'},
                {'step': 2, 'action': 'Build savings to 3 months expenses', 'target': 10000, 'time': '6-12 months'},
                {'step': 3, 'action': 'Start investing in retirement', 'target': '10% of income', 'time': 'ongoing'}
            ]
        elif stage == 'stage_3':
            return [
                {'step': 1, 'action': 'Maximize retirement contributions', 'target': 'tax-advantaged limits', 'time': 'ongoing'},
                {'step': 2, 'action': 'Diversify investments', 'target': 'balanced portfolio', 'time': '1-2 years'},
                {'step': 3, 'action': 'Increase income through skills', 'target': '+$20,000/year', 'time': '1-2 years'}
            ]
        else:
            return [
                {'step': 1, 'action': 'Scale successful investments', 'target': 'compound growth', 'time': 'ongoing'},
                {'step': 2, 'action': 'Build multiple income streams', 'target': '3+ sources', 'time': '2-5 years'},
                {'step': 3, 'action': 'Optimize tax strategy', 'target': 'minimum tax burden', 'time': 'ongoing'}
            ]
    
    def estimate_stage_time(self, stage: str) -> str:
        """Estimate time to complete stage"""
        estimates = {
            'stage_1': '6-12 months',
            'stage_2': '1-2 years',
            'stage_3': '3-5 years',
            'stage_4': '5-10 years'
        }
        
        return estimates.get(stage, 'unknown')
    
    def estimate_time_to_target(self, current: int, target: int) -> str:
        """Estimate time to reach target"""
        if current >= target:
            return 'Target reached'
        
        if current < 1000:
            return '10-15 years'
        elif current < 10000:
            return '8-12 years'
        elif current < 100000:
            return '5-8 years'
        else:
            return '3-5 years'

class FinancialEducator:
    """Educate users on financial concepts"""
    
    def __init__(self):
        self.education_modules = {
            'basics': ['budgeting', 'saving', 'credit'],
            'investing': ['stocks', 'bonds', 'mutual_funds', 'etfs'],
            'advanced': ['tax_optimization', 'real_estate', 'business_ownership']
        }
    
    def explain_concept(self, concept: str, complexity: str = 'simple') -> Dict:
        """Explain financial concept simply"""
        explanations = {
            'credit_score': {
                'simple': 'Your credit score is like a financial GPA. Higher scores mean banks trust you more and give you better interest rates on loans.',
                'detailed': 'Credit scores range from 300-850. They are calculated based on payment history (35%), credit utilization (30%), length of credit history (15%), types of credit (10%), and new credit (10%).'
            },
            'compound_interest': {
                'simple': 'Compound interest is when your money earns money, and that money earns more money. It\'s like a snowball rolling downhill, getting bigger and bigger.',
                'detailed': 'Compound interest is calculated on both the initial principal and the accumulated interest. The formula is A = P(1 + r/n)^(nt), where A is the final amount, P is principal, r is interest rate, n is compounding frequency, and t is time.'
            },
            'debt_to_income': {
                'simple': 'This ratio shows how much of your income goes to debt payments. Lower is better - ideally under 30%.',
                'detailed': 'Debt-to-income ratio is calculated by dividing total monthly debt payments by gross monthly income. Lenders prefer ratios below 36%, with under 30% being ideal.'
            },
            'emergency_fund': {
                'simple': 'Money saved for unexpected expenses like car repairs or medical bills. Aim for 3-6 months of expenses.',
                'detailed': 'An emergency fund should cover 3-6 months of essential expenses and be kept in a liquid, low-risk account like a high-yield savings account.'
            }
        }
        
        if concept in explanations:
            return {
                'concept': concept,
                'explanation': explanations[concept][complexity],
                'complexity': complexity
            }
        
        return {'error': 'Concept not found'}
    
    def generate_learning_path(self, user_id: str, current_knowledge: str) -> Dict:
        """Generate personalized learning path"""
        if current_knowledge == 'beginner':
            modules = ['budgeting', 'saving', 'credit', 'emergency_fund']
        elif current_knowledge == 'intermediate':
            modules = ['stocks', 'bonds', 'mutual_funds', 'compound_interest']
        else:
            modules = ['tax_optimization', 'real_estate', 'business_ownership']
        
        return {
            'user_id': user_id,
            'current_knowledge': current_knowledge,
            'learning_modules': modules,
            'estimated_completion': f'{len(modules) * 2} weeks',
            'generated_at': datetime.now().isoformat()
        }

class FinancialIntelligence:
    """Integrated financial intelligence system"""
    
    def __init__(self):
        self.financial_analyzer = FinancialAnalyzer()
        self.spending_analyzer = SpendingAnalyzer()
        self.opportunity_finder = OpportunityFinder()
        self.wealth_builder = WealthBuilder()
        self.financial_educator = FinancialEducator()
    
    def complete_financial_analysis(self, user_id: str, financial_data: Dict, spending_data: List[Dict], user_profile: Dict) -> Dict:
        """Complete financial analysis and wealth plan"""
        # Analyze financial health
        health = self.financial_analyzer.analyze_financial_health(user_id, financial_data)
        
        # Analyze spending
        spending = self.spending_analyzer.analyze_spending(user_id, spending_data)
        
        # Find opportunities
        opportunities = self.opportunity_finder.find_opportunities(user_id, user_profile, financial_data)
        
        # Create wealth plan
        current_savings = financial_data.get('savings', 0)
        wealth_plan = self.wealth_builder.create_wealth_plan(user_id, current_savings)
        
        # Generate education path
        education = self.financial_educator.generate_learning_path(user_id, user_profile.get('financial_knowledge', 'beginner'))
        
        return {
            'user_id': user_id,
            'financial_health': health,
            'spending_analysis': spending,
            'opportunities': opportunities,
            'wealth_plan': wealth_plan,
            'education_path': education,
            'analyzed_at': datetime.now().isoformat()
        }

# For production, we'll implement:
# - Real financial API integrations (Plaid, credit bureaus)
# - Investment portfolio tracking
# - Real-time market data
# - Tax calculation engines
# - Retirement planning calculators
# - Risk assessment models
# - Automated budget tracking
# - Bill payment automation
# - Investment rebalancing
# - Tax-loss harvesting
# - Real estate analysis tools
# - Business opportunity matching
# - Income optimization strategies

if __name__ == '__main__':
    print("Financial intelligence system ready")
