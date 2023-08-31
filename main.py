import os
import openai

openai.api_key =  "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"
astica_api_key = "BE3F19BC-4856-4311-9A2F-8E4926864CFFC10AC671-5D42-4DA1-A6F6-203AB5EF2942"


def website_responses(system_content, text, desc, html):
    text_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": system_content
            },
            {
            "role": "system",
            "content": "The reperesentation of the website you will be given is all the text on the page in relative order. "
            },
            {
            "role": "user",
            "content": text
            }
        ],
        temperature=0,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )

    description_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": system_content
            },
            {
            "role": "system",
            "content": "The reperesentation of the website you will be given is a description of the website by an ai"
            },
            {
            "role": "user",
            "content": desc
            }
        ],
        temperature=0,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )

    html_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": system_content
            },
            {
            "role": "system",
            "content": "The reperesentation of the website you will be given is in HTML"
            },
            {
            "role": "user",
            "content": html
            }
        ],
        temperature=0,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )

    return text_response['choices'][0]['message']['content'] + description_response['choices'][0]['message']['content'] + html_response['choices'][0]['message']['content']


def p1(system_content, html, website_goal):
    html_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": system_content
            },
            {
            "role": "system",
            "content": website_goal
            },
            {
            "role": "system",
            "content": "The reperesentation of the website you will be given is in HTML. You are a constructive website critic and I want you to give the website a score between 1 and 100 based on how well it does its job. Then I want you to list out 5 ways to improve this website."
            },
            {
            "role": "user",
            "content": html
            }
        ],
        temperature=0,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )

    return html_response['choices'][0]['message']['content']


def p2(system_content, html, website_goal):
    html_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": system_content
            },
            {
            "role": "system",
            "content": website_goal
            },
            {
            "role": "system",
            "content": "You will be given an html website, the goal of this website, a score for this website's design, and then 5 ways to improve this website. I want you to apply these improvements and return a new version of the html in an attempt to make the score better. If you are not given an initial html, I want you to make an html website from scratch that tries to achieve the goals given"
            },
            {
            "role": "user",
            "content": html
            }
        ],
        temperature=0,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )

    return html_response['choices'][0]['message']['content']


# Given html string, find all links and give list of tuples 
def locate_links(html):
    token_string = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": "You are a helpful assistant. You will receive a website in html format and I want you to describe what each link does. Make sure your description for each link is detailed and separate the descriptions for the links with a %."
            },
            {
            "role": "user",
            "content": html
            }
        ],
        temperature=0,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
    tokens = list(token_string['choices'][0]['message']['content'].split("%"))
    return tokens


def iterate_website(system_content, website_goal, flag, filename, iterations):
    r1 = ""
    r2 = ""
    for i in range(iterations):
        r1 = p2(system_content, r2, website_goal)
        r2 = p1(system_content, r1, website_goal)
        f = open(filename + str(i) + '.html', 'w')
        f.write(r1)
        f.close

        f = open(filename + str(i) + 'v2.html', 'w')
        f.write(r2)
        f.close

        if flag:
            toks = locate_links(r1)
            for tok in toks:
                iterate_website(system_content, "This is a linked page off of a green and white website that teaches german called germanizer. the description for this linked page is: " + tok, False, filename + "sub", 3)

    
    return r2


system_content = "Good website design is critical. Whitespace must look clean, the text must be balanced, and important things must be bold and easier to see. Users should have a very easy time navigating the website and it should be clear what the purpose of the website is. "
website_goal = "The goal of this website is that it teaches you elementary german. The website is called Germanizer and its color scheme is to be white and green. I want you to include lesson plans and an improvement calendar among other features. I want a complex webpage with a lot of features that will draw users in. "


iterate_website(system_content, website_goal, True, "tst", 5)


























'''
text_0 = "create a positng my account event calendar help faq legal activities artists new york lost+found connections childcare musicians ptets events general politics rants raves rideshare volunteeers"
desc_0 = "This is a screenshot of a web page, featuring a graphical user interface with an application table. The background color is white and the text font used in the table is black. At the top of the page there are several text menus, each containing different options for navigation. In the center of the page there is an application table which contains various numbers and labels that can be used to access information about different topics or items. On either side of this table are two columns filled with additional data such as dates, times, locations, etc., all written in black font against a white background. Below this main section are more rows containing further details related to whatever topic or item was selected from one of the menus at the top of the page. This image provides insight into how users interact with applications through tables and other graphical elements on web pages."
html_0 = "None given"
text_1 = "create a positng my account event calendar help faq legal activities artists new york lost+found connections childcare musicians ptets events general politics rants raves rideshare volunteeers"
desc_1 = "featuring a calendar with numbers and letters. The background of the image is white, and the dominant colors are also white. There appears to be some handwriting on the screen as well as text that reads application. In the center of the screen there is an open window displaying a calendar with various dates written in black ink. To the right side of this window there is another smaller window which displays more text and symbols. On either side of these windows are two thin vertical bars which appear to be part of an application or program running on this computer. At the top left corner there is what looks like a small phone icon, indicating that this could be a mobile device being used for taking screenshots or other activities related to applications or programs. Overall, this image captures an interesting moment in time where technology meets creativity - it's both functional and aesthetically pleasing at once!"
html_1 = "None given"


for i in range(6):
    system_content = "You are a user giving feedback to improve the design of a website. On a scale from one to five, your technical proficiency is a " + str(i) + " where 1 is somebody who has never used a computer and 5 is a computer expert. Give a rating to the website between 1 and 100, and give a 5 point explanation of pros and cons as to why you gave this score. \n Some general rules of thumb are: 1.  A good website should be easy to navigate. 2.  Have a clear indication of where the user is. 3. URL should be easy to remember4.  Website should be easy to search for 5.  Layout consistency is key 6. Eliminate Clutter 7.  Have the SSL encrypted pages if dealing with monetary transactions. 8. The website also can't be too empty. 9. The user must be easily capabale of completing the task provided in the description of the website. "
    responses_0 = "The first implementations feedback is this: " + website_responses(system_content, text_0, desc_0, html_0)
    responses_1 = "The second implementations feedback is this: " + website_responses(system_content, text_1, desc_1, html_1)
    
    system_task = "You are a website user. You will be given feedback from a trusted source on two different design implementations of this website. The feedback will come in three parts, one based on the text, one based on the description, and one based on the html. I want you to compare the feedback from these two implementations and tell me which implementation is better and why. "

    comparison = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "system",
        "content": system_task
        },
        {
        "role": "user",
        "content": responses_0 + responses_1
        }
    ],
    temperature=0,
    max_tokens=500,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )

    print(comparison['choices'][0]['message']['content'] + '\n\n')
'''