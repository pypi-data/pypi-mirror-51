def fix(string):
    return string.ljust(22, ' ')


profile = {'name': "Vibhu Agarwal",
           'location': "Noida, India",
           'title': "Python and Open Source Enthusiast | Web Developer",
           'summary': """{}: Back-End Web Develoment
{}: Web-Scraping, Python - Testing & Packaging
{}: Machine Learning, GCP and Desktop App. Development
{}: Working with projects which could help me learn something new
{}: Summer Internships (1-2 months)""".format(fix('Primary area of work'),
                                              fix('Greatly Involved with'),
                                              fix('Also worked on'),
                                              fix('Interested in'),
                                              fix('Looking For')),
           'need': """Hit me up anytime if you've got an interesting project and need help with anything.
If the codebase is in alien language, I can still make contributions by documenting it.""",
           'skills': ['Web Development',
                      'SQL',
                      'Machine Learning',
                      'Python Testing',
                      'Python Packaging',
                      'Browser and Task Automation']}

education = {'university': """Jaypee Institute of Information Technology, Noida
             - Computer Science and Engineering - Integrated (B.Tech. & M.Tech.)
             - 2017-Present (Current Semester: IV)""",
             'school': """St.Joseph's College, Allahabad
             - XII (I.S.C.) - 2017
             - X (I.C.S.E.) - 2015"""}

contact = {'Telegram': "vibhu4agarwal",
           'Mail': "vibhu4agarwal@gmail.com"}

tech_profiles = {'LinkedIn': "https://www.linkedin.com/in/vibhu4agarwal/",
                 'GitHub': "https://github.com/Vibhu-Agarwal"}
                 # 'Codechef': "https://www.codechef.com/users/vibhu4agarwal"}

blog = 'vibhu-agarwal.blogspot.com'

internity = {'company': "Internity Foundation",
             'role': "Machine Learning Intern",
             'time': '12/2018 - 01/2019'}

geeksforgeeks = {'company': "GeeksforGeeks",
                 'role': "Technical Content Scripter (Intern)",
                 'time': "03/2019 - 04/2019"}

creesync = {'company': "Creesync Software", 'role': "Back-End Web Developer (Intern)", 'time': "06/2019 - Present"}

work_exp = [creesync, geeksforgeeks, internity]

open_source = {
    'Marauders': {'org_name': 'Marauders',
                  'repo_links': ['https://github.com/Marauders-9998/Marauders-Website',
                                 'https://github.com/Marauders-9998/Attendance-Management-using-Face-Recognition'],
                  'role': 'Owner'},
    'pandas': {'org_name': 'pandas-dev',
               'repo_links': ['https://github.com/pandas-dev/pandas'],
               'role': 'Contributor'},
    'kivy': {'org_name': 'kivy',
             'repo_links': ['https://github.com/kivy/plyer'],
             'role': 'Contributor'},
    'nexB': {'org_name': 'nexB',
             'repo_links': ['https://github.com/nexB/scancode-toolkit'],
             'role': 'Contributor'}
}

organizations = {
    'DSC': {
        'org_name': 'Developer Student Clubs',
        'role': 'Technical Coordinator',
        'location': 'JIIT, Noida'
    }
}

projects = {
    'MOSPI Website': {
        'name': 'Ministry of Statistics and Programme Implementation (MOSPI) - Website',
        'desc': ['A Django powered Website made for MOSPI to automate the tasks'
                 ' and reduce loads of their manual work to read the excel sheets, re-'
                 ' plot them, make calculations, report statements and view insights.',
                 'Developed during Smart India Hackathon 2019'],
        'date': '03/2019',
        'link': None
    },
    'Stock Market Predictor': {
        'name': 'Stock Market Predictor',
        'desc': ['Worked on Recurrent Neural Networks and LSTMs on Time Series'
                 ' data to extract information about the future stock market trends.',
                 'Worked on this project during internship at Internity'],
        'date': '01/2019',
        'link': 'https://github.com/Vibhu-Agarwal/Stock-Market-Prediction'
    },
    'Potter Spells': {
        'name': 'Potter Spells',
        'desc': ['A python package which uses Beautiful Soup to scrape Harry Potter'
                 ' Spells and enchantments from its wiki website and provides'
                 ' content to user, also providing options for various filters to filter'
                 ' out the big chunk of data scraped from the website.'],
        'date': '07/2018',
        'link': 'https://pypi.org/project/potter-spells/'
    },
    'AMFR': {
        'name': 'Attendance Management using Face Recognition',
        'desc': ['A desktop application to manage the attendance management'
                 ' system of an institute through facial recognition.',
                 'Used openCV libraries for face detection and recognition and'
                 ' maintained data in excel files through python scripts.'],
        'date': '07/2018',
        'link': 'https://github.com/Marauders-9998/Attendance-Management-using-Face-Recognition'
    },
    'Automated FB Post': {
        'name': 'Automated Facebook Post (Speech-to-Text)',
        'desc': ['Used browser automation in python and wit.ai for speech-to-text'
                 ' conversion to post on Facebook through voice or audio.'],
        'date': '03/2018',
        'link': 'https://github.com/Vibhu-Agarwal/Automated-Facebook-Post-from-Speech-to-Text'
    }
}
