"""Reproducible illustrative project model. Standard library only; nominal JOD.
No inputs are noon internal data or binding partner quotes. Run from any directory.
"""
from pathlib import Path
import json, math
ROOT=Path(__file__).resolve().parents[1]
INPUTS={
 'years':[2027,2028,2029], 'orders':[60000,150000,240000],
 'customers':[20000,40000,60000], 'orders_per_customer':[3,3.75,4],
 'aov':45, 'commission':0.15, 'delivery_fee':3, 'payment_rate':0.02,
 'logistics_per_order':[7,4.8,4.5], 'handling_loss_reserve_per_order':[0.9,0.7,0.6],
 'staff':[144000,216000,264000], 'marketing':[72000,108000,132000],
 'platform_support':[48000,66000,72000], 'rent_advisers_admin':[36000,60000,72000],
 'setup':[100000,0,0], 'capex':[90000,90000,30000], 'capex_life_years':3,
 'nwc_closing':[40000,100000,160000], 'equity_injection':[600000,300000,0],
 'tax_scenario_rate':0.21,
 'first_year_monthly_orders':[1000,2000,3000,3000,4000,5000,5000,6000,6000,7000,8000,10000],
 'sales_mix':[{'category':'Home accessories, non-electrical','order_share':0.4,'basket':50},
              {'category':'Fashion accessories','order_share':0.35,'basket':40},
              {'category':'Phone accessories, non-powered','order_share':0.25,'basket':44}],
}
def calc(orders,aov,commission,logistics,reserve,fixed,depreciation,setup=0):
    gmv=orders*aov
    commission_rev=gmv*commission
    delivery_rev=orders*INPUTS['delivery_fee']
    revenue=commission_rev+delivery_rev
    payment=gmv*INPUTS['payment_rate']
    handling=orders*reserve
    logistics_cost=orders*logistics
    contribution=revenue-payment-handling-logistics_cost
    ebitda=contribution-fixed-setup
    ebit=ebitda-depreciation
    tax=max(ebit,0)*INPUTS['tax_scenario_rate']
    return dict(orders=orders,gmv=gmv,commission_revenue=commission_rev,delivery_revenue=delivery_rev,
                revenue=revenue,payment_cost=payment,handling_reserve=handling,logistics_cost=logistics_cost,
                variable_cost=payment+handling+logistics_cost,contribution=contribution,
                contribution_per_order=contribution/orders,fixed_cost=fixed,setup=setup,
                ebitda=ebitda,depreciation=depreciation,ebit=ebit,tax=tax,net_profit=ebit-tax)
def build():
    a=INPUTS; annual=[];cash=ppe=equity=retained=0;nwc_previous=0
    for i,year in enumerate(a['years']):
        fixed=sum(a[k][i] for k in ['staff','marketing','platform_support','rent_advisers_admin'])
        dep=sum(a['capex'][:i+1])/a['capex_life_years']
        row=calc(a['orders'][i],a['aov'],a['commission'],a['logistics_per_order'][i],a['handling_loss_reserve_per_order'][i],fixed,dep,a['setup'][i])
        row['year']=year;row['cash_opening']=cash
        row['delta_nwc']=a['nwc_closing'][i]-nwc_previous
        row['capex']=a['capex'][i];row['equity_injection']=a['equity_injection'][i]
        row['operating_cash_flow']=row['ebitda']-row['tax']-row['delta_nwc']
        row['free_cash_flow']=row['operating_cash_flow']-row['capex']
        cash+=row['free_cash_flow']+row['equity_injection'];ppe+=row['capex']-dep
        equity+=row['equity_injection'];retained+=row['net_profit']
        row.update(cash_closing=cash,nwc=a['nwc_closing'][i],net_ppe=ppe,paid_equity=equity,
                   retained_earnings=retained,net_assets=cash+ppe+a['nwc_closing'][i],total_equity=equity+retained)
        nwc_previous=a['nwc_closing'][i];annual.append(row)
    monthly=[];cash=0
    for i,year in enumerate(a['years']):
        orders=a['first_year_monthly_orders'] if i==0 else [a['orders'][i]/12]*12
        for month,n in enumerate(orders,1):
            ar=annual[i];contrib=n*ar['contribution_per_order'];fixed=ar['fixed_cost']/12
            setup=ar['setup'] if month==1 else 0
            capex=ar['capex'] if month==1 else 0
            dnwc=ar['delta_nwc'] if month==1 else 0
            funding=ar['equity_injection'] if month==1 else 0
            tax=ar['tax']/12  # planning cash provision, not statutory instalment dates
            opening=cash;cash+=funding+contrib-fixed-setup-capex-dnwc-tax
            monthly.append(dict(year=year,month=month,orders=n,opening_cash=opening,funding=funding,
                                contribution=contrib,fixed=fixed,setup=setup,capex=capex,delta_nwc=dnwc,
                                tax_provision=tax,closing_cash=cash))
    cases=[('Base',240000,45,.15,4.5,.6),('Orders 25% lower',180000,45,.15,4.5,.6),
           ('Logistics JOD 1 higher',240000,45,.15,5.5,.6),('Commission 12%',240000,45,.12,4.5,.6),
           ('Basket 10% lower',240000,40.5,.15,4.5,.6),
           ('Combined downside',180000,45,.12,5.5,.6)]
    sensitivity=[dict(case=label,**calc(n,b,c,l,r,540000,70000)) for label,n,b,c,l,r in cases]
    # Independent identities and exact expected outcomes catch scale/netting mistakes.
    checks=[]
    def check(name,ok):
        assert ok,name; checks.append(name)
    check('Category-weighted AOV equals JOD 45',math.isclose(sum(x['basket']*x['order_share'] for x in a['sales_mix']),45))
    check('Monthly first-year orders sum to 60,000',sum(a['first_year_monthly_orders'])==60000)
    for i,r in enumerate(annual):
        check(f'{r["year"]}: customers times frequency equals orders',a['customers'][i]*a['orders_per_customer'][i]==r['orders'])
        check(f'{r["year"]}: GMV differs from net platform revenue',math.isclose(r['revenue'],r['gmv']*.15+r['orders']*3))
        check(f'{r["year"]}: cash roll-forward',math.isclose(r['cash_opening']+r['net_profit']+r['depreciation']-r['delta_nwc']-r['capex']+r['equity_injection'],r['cash_closing']))
        check(f'{r["year"]}: net asset/equity balance',math.isclose(r['net_assets'],r['total_equity']))
        check(f'{r["year"]}: monthly and annual cash reconcile',math.isclose(monthly[(i+1)*12-1]['closing_cash'],r['cash_closing']))
    check('Base closing cash JOD 538,600',math.isclose(annual[-1]['cash_closing'],538600))
    check('Three-year free cash flow is negative JOD 361,400',math.isclose(sum(r['free_cash_flow'] for r in annual),-361400))
    check('2029 net profit JOD 229,100',math.isclose(annual[-1]['net_profit'],229100))
    check('Combined downside EBIT negative JOD 358,000',math.isclose(sensitivity[-1]['ebit'],-358000))
    check('Lowest monthly base cash JOD 127,000',math.isclose(min(m['closing_cash'] for m in monthly),127000))
    return dict(inputs=a,annual=annual,monthly=monthly,sensitivity=sensitivity,
                break_even={'cash_orders_2029':540000/3.75,'accounting_orders_2029':610000/3.75},
                checks=checks,check_count=len(checks),
                limitations=['No actual supplier quotes or company internal data.',
                             'All tax, duty, ownership, working-capital and service assumptions require validation.',
                             'Whole-project economic view; no JV consolidation or investor-specific returns.',
                             'No inventory financing, seller settlement float, debt or dividends assumed.',
                             'Annual capex, funding and working-capital increase occur in January.',
                             'Operating cash is distributed monthly; tax cash provision is smoothed, not a legal payment schedule.',
                             'No value ascribed after 2029; no NPV or IRR claimed.'])
if __name__=='__main__':
    data=build();(ROOT/'financial_model.json').write_text(json.dumps(data,indent=2)+'\n')
    print(f'{data["check_count"]} finance checks passed; final cash {data["annual"][-1]["cash_closing"]:,.2f} JOD')
