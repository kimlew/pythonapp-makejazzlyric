from flask import Flask, render_template, request
from datetime import datetime
from connVarsDict import connDict
import mysql.connector

app = Flask(__name__)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    msg_params = {
        "need_vowel1_msg" : "",
        "need_vowel2_msg": "",
        "need_number_msg" : "",
        "need_consonant_msg" : ""
    }
    return render_template('create_lyric.html', the_title='Create a Jazz '
                                                         'Lyric', the_msg_params=msg_params,)


@app.route('/show_lyric', methods=['POST'])
def create_lyric() -> str:
    title = 'New Jazz Lyric'
    vowel_set = list('aeiouy')
    consonant_set = list('bcdfghijklmnpqrstvwxz')

    need_vowel_msg = 'You must enter a vowel.'
    need_number_msg = 'You must enter a number from 3-9.'
    need_consonant_msg = 'You must enter a consonant.'

    vowel1 = request.form['vowel1'].lower()
    vowel2 = request.form['vowel2'].lower()
    vowel2_amount = 0

    # Add try-catch block for when this field is empty string, ''.
    try:
        vowel2_amount = int(request.form['vowel2_amount'])
    except:
        print(Exception)

    consonant = request.form['consonant'].lower()

    error_count = 0

    msg_params = {
        "need_vowel1_msg": "",
        "need_vowel2_msg": "",
        "need_number_msg": "",
        "need_consonant_msg": ""
    }

    if vowel1 not in vowel_set:
        # Render entry page again & print('Enter a vowel.')
        print("vowel1 is: ", vowel1)
        print("vowel_set is: ", vowel_set)
        error_count += 1
        msg_params["need_vowel1_msg"] = need_vowel_msg

    elif vowel2 not in vowel_set:
        # Render entry page again & print('Enter a vowel.')
        error_count += 1
        msg_params["need_vowel2_msg"] = need_vowel_msg

    elif vowel2_amount < 3 or vowel2_amount > 9:
        # Render entry page again & print('Enter a number from 3-9.')
        error_count += 1
        msg_params["need_number_msg"] = need_number_msg

    elif consonant not in consonant_set:
        # Render entry page again & print('Enter a consonant.')
        error_count += 1
        msg_params["need_consonant_msg"] = need_consonant_msg

    if error_count == 1 or error_count == 2 or error_count == 3 or \
                error_count == 4:
        return render_template('create_lyric.html', the_title='Create a Jazz Lyric', the_msg_params=msg_params, )

    # Shoo dap ba diii *eeeeeee...
    lyric = " Shooo" +\
            " d" + (vowel1) + "p" +\
            " b" + (vowel1 * 2) + " " +\
            consonant + (vowel2 * int(vowel2_amount)) +\
            " z" + ("e" * 8) + \
            "... "

    try:
        conn = mysql.connector.connect(**connDict)
        cursor = conn.cursor()

        nowdatetime = datetime.now()

        _SQL = """INSERT INTO lyric(lyric, date_created) VALUES (%s, %s)"""
        cursor.execute(_SQL, (lyric, nowdatetime))

        conn.commit()
    finally:
        conn.close()

    vowel_count = count_vowels(lyric)
    lyric_params = {
        "the_title" :  title,
        "the_vowel1" : vowel1,
        "the_vowel2" : vowel2,
        "the_vowel2_amount" : vowel2_amount,
        "the_consonant" : consonant,
        "the_lyric" : lyric,
        "the_vowel_count" : vowel_count
    }

    return render_template('show_lyric.html', the_lyric_params=lyric_params,)


def count_vowels(lyric) -> str:
    vowels = set('aeiouy')
    vowel_count = 0

    for item in lyric:
        if item in vowels:
            vowel_count = vowel_count + 1

    return vowel_count


def add_lyric_to_db() -> str:
    # Establish connection & create cursor.
    conn = mysql.connector.connect(**connDict)
    cursor = conn.cursor()


@app.route('/show_song', methods=['GET','POST'])
def create_song() -> str:
    title = 'Jazz Song'
    a_lyric = ''
    date_created = ''

    try:
        conn = mysql.connector.connect(**connDict)
        cursor = conn.cursor()

        _SQL = """SELECT lyric, 
            EXTRACT(YEAR FROM date_created), 
            EXTRACT(MONTH FROM date_created), 
            EXTRACT(DAY FROM date_created) 
            FROM lyric WHERE date_deactivated IS NULL"""

        conn.commit()
    finally:
        conn.close()
    #
    # Use loop & retrieve
    # def show_song()
    #     for each row in lyric table
    #     SELECT
    #     lyric, EXTRACT(YEAR, MONTH, DAY
    #     FROM
    #     date_created) WHERE
    #     date_deactivated is NOT
    #     NULL
    #     if row number is divisible by 4:
    #         print('\n')
    #   return all of that somehow.

    song_params = {
        "the_title" :  title,
        "a_lyric": a_lyric,
        "the_date_created": date_created
    }
    return render_template('show_song.html', the_song_params=song_params,)


if __name__ == '__main__':
    #  app.config['dbconfig'] = connDict

    # Test with:
    # Import driver, establish connection & create cursor.

    # Put in main() temporarily - so runs immediately to see if MySQL works.
    # If I put in Flask handler function that handles it for the page,
    # I would have to run so it goes to the show_lyric page.

    # conn = mysql.connector.connect(**connDict)
    # cursor = conn.cursor()

    # _SQL = """SHOW DATABASES"""
    # cursor.execute(_SQL)
    # res = cursor.fetchall()
    # for row in res:
    #     print(row)

    app.run(debug=True)
