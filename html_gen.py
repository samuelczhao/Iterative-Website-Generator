import os
import openai

openai.api_key =  "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"
astica_api_key = "BE3F19BC-4856-4311-9A2F-8E4926864CFFC10AC671-5D42-4DA1-A6F6-203AB5EF2942"


UX_PERSONA = "I want you to act as a UX/UI developer. I will provide some details about the design of an app, website or other digital product, and it will be your job to write html for the website and come up with creative ways to improve its user experience."
DESIGN_RULES = open("design_rules.txt", "r").read()


def write_html_to_file(html, filename):
    f = open(filename + '.html', 'w')
    f.write(html)
    f.close
    

# Generate a first pass version of the website
def base_html(website_goal, website_name):
    html = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user",
        "content": DESIGN_RULES},
        {"role": "user",
        "content": website_goal},
        {"role": "user",
        "content": "I want you to generate the html for a website that achieves all the goals given above while also taking into account the rules of website design."},
        {"role": "system",
        "content": UX_PERSONA}
    ],
    temperature=0,
    max_tokens=2000,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )['choices'][0]['message']['content']

    filename = website_name + "_homepage_v0"
    write_html_to_file(html, filename)
    print(filename)


# Return feedback for an html page given prior feedback. 
def html_feedback(html, prior_feedback, website_goal):
    print(html)
    print(prior_feedback)
    print(website_goal)
    print(DESIGN_RULES)
    feedback = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
            "content": website_goal},
            {"role": "user",
            "content": prior_feedback},
            {"role": "user",
            "content": DESIGN_RULES},
            {"role": "user",
            "content": html},
            {"role": "user",
            "content": "The reperesentation of the website you will be given is in HTML. Then I want you to list out 5 ways to improve this website that are not already in the prior feedback."}
        ],
        temperature=0,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )['choices'][0]['message']['content']

    return feedback

def improve_base_html(html, website_goal, filename, new_feedback, prior_feedback):
    iter_html = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
            "content": website_goal},
            {"role": "user",
            "content": prior_feedback},
            {"role": "user",
            "content": new_feedback},
            {"role": "user",
            "content": DESIGN_RULES},
            {"role": "user",
            "content": html},
            {"role": "system",
            "content": "The reperesentation of the website you will be given is in HTML. You are a constructive website critic and I want you to give the website a score between 1 and 100 based on how well it does its job. Then I want you to list out 5 ways to improve this website."}
        ],
        temperature=0,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )['choices'][0]['message']['content']

    write_html_to_file(html, filename)
    return iter_html


# Given html string, find all links and give list of tuples 
def locate_links(html):
    token_string = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
            "content": html},
            {"role": "system",
            "content": "You are a helpful assistant. You will receive a website in html format and I want you to describe what each link does. Make sure your description for each link is detailed and separate the descriptions for the links with a %."}
        ],
        temperature=0,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
    tokens = list(token_string['choices'][0]['message']['content'].split("%"))
    return tokens


def iterate_website(website_goal, website_name, flag, iterations):
    html = base_html(website_goal, website_name)
    feedback = ""
    prior_feedback = ""
    for i in range(iterations):
        filename = website_name + "homepage_v" + str(i + 1) + ".html"
        feedback = html_feedback(html, prior_feedback, website_goal)
        html = improve_base_html(html, website_goal, filename, feedback, prior_feedback)
        prior_feedback += feedback
        '''
        if flag:
            toks = locate_links(html)
            for tok in toks:
                iterate_website(system_content, "This is a linked page off of a green and white website that teaches german called germanizer. the description for this linked page is: " + tok, False, filename + "sub", 3)
        '''
    return html