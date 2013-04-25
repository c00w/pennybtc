from webserver import *

@app.route('/request_charge', methods=['GET'])
def request_charge():
    return render_template('charge.html', key=stripe_key['publishable_key'], amount=500, amount_usd="$5.00", name="retard")


@app.route('/process_charge', methods=['POST'])
def charge():
    #amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email='customer@example.com',
        card=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('thanks.html', amount=amount)
