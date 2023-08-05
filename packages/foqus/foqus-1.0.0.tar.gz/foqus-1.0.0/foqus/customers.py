import uuid
import datetime


from foqus.aws_configuration import *
from foqus.azure_configuration import *
from foqus.database import *

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib

import codecs
import logging
import coloredlogs

if LOCAL is False:

    from azure_storage_logging.handlers import TableStorageHandler

    # configure the handler and add it to the logger
    logger = logging.getLogger(__name__)
    handler = TableStorageHandler(account_name=LOG_AZURE_ACCOUNT_NAME,
                                  account_key=LOG_AZURE_ACCOUNT_KEY,
                                  extra_properties=('%(hostname)s',
                                                    '%(levelname)s'))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
else:

    logger = logging.getLogger(__name__)
    coloredlogs.install()
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(LOG_PATH + 'trynfit_debug.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s', '%d/%b/%Y %H:%M:%S')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

# Starting connection
db = PostgreSQL()
# db.create_users_management_table()


def send_email_to_admin(subject, message):

    try:
        logger.info("start sending email ...")
        server = smtplib.SMTP('smtp.sendgrid.net', 587)
        server.login(SENDGRID_USERNAME, SENDGRID_PASSWORD)
        fromaddr = "FOQUS <contact@trynfit.com>"
        toaddr = "dbellarej@trynfit.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject
        body = message
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        logger.info("End of sending email to admin ")
    except Exception as e:
        logger.info("exception in sending email to admin  ..." + str(e))


def send_inscription_email(customer_email, full_url, password_client):

    try:
        logger.info("start sending inscription  email ...")
        server = smtplib.SMTP('smtp.sendgrid.net', 587)
        server.login(SENDGRID_USERNAME, SENDGRID_PASSWORD)
        fromaddr = "FOQUS <contact@trynfit.com>"
        toaddr = customer_email
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = 'Activez votre compte FOQUS'
        html_file = codecs.open(PATH_INSCRIPTION_EMAIL_CUSTOMER, 'r')
        html = (str(html_file.read()).replace("#full_url", (full_url)).replace("#password", password_client))
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        logger.info("End of sending inscrition email for client %s" %customer_email)
    except Exception as e:
        logger.info("exception in sending email ..." + str(e))


def send_email(customer_name, subject):

    customer_profile = db.get_customer_info_from_customer_name(customer_name=customer_name)
    for custmer in customer_profile:
        customer_email = custmer[3]

        try:
            logger.info("start sending email ...")
            server = smtplib.SMTP('smtp.sendgrid.net', 587)
            server.login(SENDGRID_USERNAME, SENDGRID_PASSWORD)
            fromaddr = "FOQUS <contact@trynfit.com>"
            toaddr = customer_email
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = subject
            html_file = codecs.open(PATH_EMAIL_CUSTOMER, 'r')
            html = (str(html_file.read()).replace("#name", (customer_profile[0][9])))
            part2 = MIMEText(html, 'html')
            msg.attach(part2)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            logger.info("End of sending email ")
        except Exception as e:
            logger.info("exception in sending email ..." + str(e))


def send_email_training_started(email, project_name, customer_name, customer_type):
    # Send Email
    server = smtplib.SMTP('smtp.sendgrid.net', 587)
    server.login(SENDGRID_USERNAME, SENDGRID_PASSWORD)
    try:
        fromaddr = "FOQUS <contact@trynfit.com>"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = email
        msg['Subject'] = "Training completed"

        html_file = codecs.open(PATH_EMAIL_TRINING_STARTED_CMS, 'r')
        html = ((str(html_file.read()).replace("#name", customer_name)).replace("#type", customer_type)).replace(
            "#project", project_name)
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        server.sendmail(fromaddr, email, msg.as_string())
    except Exception as e:
        logger.error("exception ......" + str(e))


def create_or_update_user_apikey(user='anonymous', period_in_hours=72):
    db.update_customer(user, str(uuid.uuid4()), period_in_hours)
    db.commit_db_changes()


def all_status_project(customer_name, customer_type):
    result = db.select_status_project_similars(table_name="status_projects", customer=customer_name, customer_type=customer_type)
    return result


def specified_project_status(customer_name, customer_type, project_name):
    result = db.get_status_project(table_name="status_projects", customer=customer_name, customer_type=customer_type, api="similars", project=project_name)
    return result


def create_update_project(customer, customer_type, project_to_delete, api, status,name, training_details ,counter):
    table_name = "status_projects"
    db.create_status_projects_table(table_name)
    db.insert_or_update_status_projects_table(table_name, customer, customer_type, project_to_delete, api, status,name,training_details ,counter)


def customer_info(customer_email):
    try:
        customer_info = db.get_profile(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME,customerEmail=customer_email)
    except Exception as e:
        logger.error('email not found for this customer , Please verify your email  %s' %e)
        return []
    return customer_info


def is_apikey_valid(user_apikey):
    try:
        user = db.get_customer_from_apikey(apikey=user_apikey)[0]
    except:
        logger.error("APIKEY not found. Access forbidden for '" + str(user_apikey) + "'")
        return False
    return True


def is_user_allowed(user_apikey):
    try:
        user = db.get_customer_from_apikey(apikey=user_apikey)[0]
    except:
        logger.error("APIKEY not found. Access forbidden for '" + str(user_apikey) + "'")
        return False

    expiration = db.get_expiration_from_apikey(apikey=user_apikey)[0]
    if time.time() > expiration:
        logger.info("User '" + user + "' is not allowed because APIKEY has expired. Expiration date: " + time.ctime(
            int(db.get_expiration_from_customer(user)[0])))
        return False
    return True


def get_apikey_expiration(user_apikey):
    try:
        user = db.get_customer_from_apikey(apikey=user_apikey)[0]
    except:
        logger.error("APIKEY not found. Access forbidden for '" + user_apikey + "'")
        return False

    expiration = db.get_expiration_from_apikey(apikey=user_apikey)[0]
    return expiration


def get_user_apikey(customer):
    try:
        user_apikey = db.get_apikey_from_customer(customer=customer)[0]
    except:
        logger.error("Customer not found. Access forbidden for '" + customer + "'")
        return None

    expiration = db.get_expiration_from_apikey(apikey=user_apikey)[0]
    if time.time() > expiration:
        logger.error("User '" + customer + "' is not allowed because APIKEY has expired. Expiration date: " + time.ctime(
            int(db.get_expiration_from_customer(customer)[0])))
        return None
    return user_apikey


def is_customer_registered(customer):
    try:
        user_apikey = db.get_apikey_from_customer(customer=customer)[0]
    except:
        logger.error("Customer '" + customer + "' not found.")
        return False
    return True


def get_json_ads_number(json_input, customer_name, customer_type):
    return len(json_input[customer_name.lower() + '_' + customer_type.lower()])


def get_json_ad_status(json_input, customer_name, customer_type, index):
    if customer_type == 'estate':
        status = json_input[customer_name.lower() + '_' + customer_type.lower()][index]['Status']
        if status is not None and int(status) == 1:
            return 1
        else:
            return 0
    else:
        return 1


def get_json_ad_photos(json_input, customer_name, customer_type, index):
    return json_input[customer_name.lower() + '_' + customer_type.lower()][index]['Photos']


def get_json_ad_categorie(json_input, customer_name, customer_type, index):
    return json_input[customer_name.lower() + '_' + customer_type.lower()][index]['Categorie']


def save_data_from_cms(customer_name, customer_type, project_name, cms, url_shop, access_token):
    db.create_cms_table()
    try:
        db.add_or_update_cms_table(table_name="cms_client_table", customer_name=customer_name,
                                   customer_type=customer_type, project_name=project_name, cms=cms, url_shop=url_shop,
                                   token=access_token)
    except Exception as e:
        logger.error("Error in saving the data from cms %s for client %s access_token %s, error %s"
                     % (cms, customer_name, access_token, e))


def scores_repartition_per_users(customer, customer_type):
    response_list = db.select_similars_classification_result("client_history_table", customer, customer_type)
    nb_person_10_30 = 0
    nb_person_30_50 = 0
    nb_person_50_75 = 0
    nb_person_75_90 = 0
    nb_person_90_100 = 0
    if response_list != []:
        for j in range(0, len(response_list)):
            for i in range(0, len(response_list[j])):
                if i == 7:
                    if "similars" in response_list[j][i]:
                        similars = json.loads(response_list[j][i])
                        if int(similars["similars"][0]['score']) < 30:
                            nb_person_10_30 = nb_person_10_30 + response_list[j][9]
                        elif int(similars["similars"][0]['score']) > 30 and int(
                                similars["similars"][0]['score']) < 50:
                            nb_person_30_50 = nb_person_30_50 + response_list[j][9]
                        elif int(similars["similars"][0]['score']) > 50 and int(
                                similars["similars"][0]['score']) < 75:
                            nb_person_50_75 = nb_person_50_75 + response_list[j][9]
                        elif int(similars["similars"][0]['score']) > 75 and int(
                                similars["similars"][0]['score']) < 90:
                            nb_person_75_90 = nb_person_75_90 + response_list[j][9]
                        else:
                            nb_person_90_100 = nb_person_90_100 + response_list[j][9]
    else:
        logger.info("No historic detected")

    nb_person_list = [nb_person_10_30, nb_person_30_50, nb_person_50_75, nb_person_75_90, nb_person_90_100]
    return nb_person_list


def get_counter_of_last_four_months(customer, customer_type):
    today = datetime.date.today()
    first = today.replace(day=1)
    curr_month = str(today)[5:7]
    lastMonth = (first - datetime.timedelta(days=1)).strftime("%m")
    first_day_of_last_month = (first - datetime.timedelta(days=1)).replace(day=1)
    last_lastMonth = (first_day_of_last_month - datetime.timedelta(days=1)).strftime("%m")
    first_day_four_month_ago = (
        first_day_of_last_month - datetime.timedelta(days=1) - datetime.timedelta(days=1)).replace(day=1)
    fourth_month_ago = (first_day_four_month_ago - datetime.timedelta(days=1)).strftime("%m")
    last_four_last_months = [curr_month, lastMonth, last_lastMonth, fourth_month_ago]
    request_number = []
    for month in last_four_last_months:
        value = db.select_utilistation_par_mois("client_history_table", customer, customer_type, month)
        if value:
            request_number.append(value)
        else:
            request_number.append(0)
    nbr_requests_by_month = []
    for j in range(0, len(request_number)):
        nbr_requests_by_month.append((last_four_last_months[j], request_number[j]))
    return nbr_requests_by_month
