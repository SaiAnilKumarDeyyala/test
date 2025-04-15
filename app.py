from flask import Flask, render_template, request
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient import discovery

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/post_job', methods=['POST'])
def post_job():
    post_title = request.form.get('postTitle')
    image = request.form.get('image')
    tags = request.form.get('tags')
    description = request.form.get('description')
    apply_link = request.form.get('applyLink')
    adsense_code = request.form.get('adsenseCode')

    company = request.form.get('company')
    role = request.form.get('role')
    batch = request.form.get('batch')
    education = request.form.get('education')
    salary = request.form.get('salary')
    lastDate = request.form.get('lastDate')
    location = request.form.get('location')


    last_ten_posts = get_last_ten_posts()
    last_ten_links = [post['url'] for post in last_ten_posts]
    last_ten_titles = [post['title'] for post in last_ten_posts]
    last_ten_count = len(last_ten_links)

    htmlData = buildHtml(company,role,batch,education,salary,lastDate,location,post_title,image,tags,description,apply_link,adsense_code,last_ten_titles, last_ten_links)
    
    payload={
        "content": htmlData,
        "title": post_title,
        'labels': tags,
        'customMetaData': customMetaData
    }
    postedJob = postToBlogger(payload)
    link = postedJob['url']
    # Process the submitted form values as needed
    return render_template('result.html',last_ten_count=last_ten_count,last_ten_titles=last_ten_titles,last_ten_links=last_ten_links,link=link,post_title=post_title, image=image, description=description)

@app.route('/recent_posts')
def recent_posts():
        last_ten_posts = get_last_ten_posts()
        last_ten_links = [post['url'] for post in last_ten_posts]
        last_ten_titles = [post['title'] for post in last_ten_posts]
        last_ten_count = len(last_ten_links)
        return render_template('recent_posts.html',last_ten_count=last_ten_count,last_ten_titles=last_ten_titles,last_ten_links=last_ten_links)


# Start the OAuth flow to retrieve credentials
def authorize_credentials():
    CLIENT_SECRET = 'client_secret.json'
    SCOPE = 'https://www.googleapis.com/auth/blogger'
    STORAGE = Storage('credentials.storage')
    # Fetch credentials from storage
    credentials = STORAGE.get()
    # If the credentials doesn't exist in the storage location then run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials

# print(credentials)
def getBloggerService():
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://blogger.googleapis.com/$discovery/rest?version=v3')
    service = discovery.build('blogger', 'v3', http=http, discoveryServiceUrl=discoveryUrl)
    return service

def postToBlogger(payload):
    service = getBloggerService()
    post=service.posts()
    insert=post.insert(blogId='8826747196654473873',body=payload).execute()
    print("Done post!")
    return insert

def buildHtml(company,role,batch,education,salary,lastDate,location,post_title, image, tags, description, apply_link, adsense_code, last_ten_titles, last_ten_links):
    description_html = f"<pre>{description}</pre>"
    
    table_html_code = f"""
    <div class="separator" style="clear: both; text-align: left;">
        <style>
            #simple_table {{
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
                background-color: #ffffff;
                color: black;
            }}
            #simple_table td, #simple_table th {{
                text-align: left;
                padding: 8px;
                border: 1px solid #808080;
            }}
            #simple_table tr:nth-child(even) {{
                background-color: #dddddd;
            }}
            #simple_table tr:hover {{
                background-color: #ffff99;
            }}
            #simple_table tr > th {{
                background: #1b90bb;
                color: #ffffff;
            }}
        </style>
        <table id="simple_table">
            <tbody>
                <tr>
                    <th>JOB</th>
                    <th>DETAILS</th>
                </tr>
                <tr>
                    <td>Company</td>
                    <td>{company}</td>
                </tr>
                <tr>
                    <td>Role</td>
                    <td>{role}</td>
                </tr>
                <tr>
                    <td>Batch</td>
                    <td>{batch}</td>
                </tr>
                <tr>
                    <td>Education</td>
                    <td>{education}</td>
                </tr>
                <tr>
                    <td>Salary</td>
                    <td>{salary}</td>
                </tr>
                <tr>
                    <td>Last Date</td>
                    <td>{lastDate}</td>
                </tr>
                <tr>
                    <td>Location</td>
                    <td>{location}</td>
                </tr>
                				<tr>
					<td>More 2022 Batch Job Updates</td>
					<td><a href="https://www.telugutechlearners.in/search/label/2022_batch" rel="nofollow" target="_blank">CLICK HERE</a></td>
				</tr>
				<tr>
					<td>More 2023 Batch Job Updates</td>
					<td><a href="https://www.telugutechlearners.in/search/label/2023_batch" rel="nofollow" target="_blank">CLICK HERE</a></td>
				</tr>
				<tr>
					<td>More 2024 Batch Job Updates</td>
					<td><a href="https://www.telugutechlearners.in/search/label/2024_batch" rel="nofollow" target="_blank">CLICK HERE</a></td>
				</tr>
				<tr>
					<td>For Daily Job Updates</td>
					<td><a href="https://www.instagram.com/daily_job_updates_freshers/" rel="nofollow" target="_blank">CLICK HERE</a></td>
				</tr>
            </tbody>
        </table>
    </div>
    """

    if company == None or company == "":
         table_html_code = ""
    recent_posts_html = ""
    reversed_titles = list(reversed(last_ten_titles))
    reversed_links = list(reversed(last_ten_links))
    for index, title in enumerate(last_ten_titles):
        post_index = len(last_ten_titles) - index - 1
        link_text = f"<a href='{last_ten_links[post_index]}' style='text-decoration: none; animation: blink 1s infinite;'>Apply Now</a>"
        recent_posts_html += f"<p>{index+1}. {last_ten_titles[post_index]} - {link_text}</p>"

    # Inline CSS for the blinking animation
    recent_posts_html += """
    <style>
        @keyframes blink {
            0% { opacity: 0; color: red; }
            50% { opacity: 1; color: blue; }
            100% { opacity: 0; color: green; }
        }
    </style>
    """



    html = f"""
    <div id="adsense">{adsense_code}</div>
    <h1>{post_title}</h1>
    <img src="{image}" alt="{tags}"><br>
    <div>{table_html_code}</div>
    <br>
        <div class="posts">
        <h1 style="text-decoration: underline;">Companies Hiring Now:</h1>
        {recent_posts_html}
        </div><br>
    <b style="text-decoration: underline;">JOB DESCRIPTION:</b>
    <p>{description_html}</p>
    <div id="adsense">{adsense_code}</div>
    <div class="separator" style="clear: both; text-align: left;"><strike><a href="{apply_link}" rel="nofollow" target="_blank">APPLY NOW(link)</a></strike></div>
    <div class="separator" style="clear: both; text-align: left;"><br /></div>
    <div id="adsense">{adsense_code}</div>
    """
    return html


def get_last_ten_posts():
    service = getBloggerService()
    post = service.posts()
    response = post.list(blogId='8826747196654473873', maxResults=10).execute()
    last_ten_posts = response.get('items', [])
    return last_ten_posts

customMetaData = "This is meta data"


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
