from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class DonationForm(FlaskForm):
    donor_name = StringField('Donor Name', validators=[DataRequired()])
    food_type = StringField('Food Type', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    expiration_date = StringField('Expiration Date', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    contact_info = StringField('Contact Information', validators=[DataRequired()])
    submit = SubmitField('Submit Donation')

class ReceiverRequestForm(FlaskForm):
    receiver_name = StringField('Receiver Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    contact_info = StringField('Contact Information', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit Request')

food_donations = []
receiver_requests = []
notifications = []

def send_notification(donor, receiver):
    donor_name = donor.get('donor_name')
    receiver_name = receiver.get('receiver_name')

    if donor_name and receiver_name:
        donor_contact_info = donor.get('contact_info', 'No contact info')
        receiver_contact_info = receiver.get('contact_info', 'No contact info')

        notification = f"Donor ({donor_name}, Contact: {donor_contact_info}) and Receiver ({receiver_name}, Contact: {receiver_contact_info}) are available at the same location!"
        notifications.append(notification)

def check_for_notifications(new_data):
    for existing_data in food_donations + receiver_requests:
        if new_data['location'] == existing_data['location']:
            send_notification(existing_data, new_data)

@app.route('/')
def home():
    return render_template('index.html', donations=food_donations, requests=receiver_requests)

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    form = DonationForm()
    if form.validate_on_submit():
        donation = {
            'donor_name': form.donor_name.data,
            'food_type': form.food_type.data,
            'quantity': form.quantity.data,
            'expiration_date': form.expiration_date.data,
            'location': form.location.data,
            'contact_info': form.contact_info.data
        }
        food_donations.append(donation)
        check_for_notifications(donation)
        return redirect(url_for('home'))
    return render_template('donate.html', form=form)

@app.route('/request', methods=['GET', 'POST'])
def request_food():
    form = ReceiverRequestForm()
    if form.validate_on_submit():
        request_data = {
            'receiver_name': form.receiver_name.data,
            'location': form.location.data,
            'contact_info': form.contact_info.data,
            'quantity': form.quantity.data,
        }
        receiver_requests.append(request_data)
        check_for_notifications(request_data)
        return redirect(url_for('home'))
    return render_template('request_food.html', form=form)

@app.route('/notifications')
def view_notifications():
    return render_template('notifications.html', notifications=notifications)

if __name__ == '__main__':
    app.run(debug=True)