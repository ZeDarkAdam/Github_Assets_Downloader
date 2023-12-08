import streamlit as st

import requests
import math
from datetime import datetime

import time
# start_time = time.time()
# st.write(f"Execution time: {time.time() - start_time} seconds")


st.set_page_config(
    page_title="Github Assets Downloader",
    page_icon= "⬇️",
    layout="centered" # wide, centered
)

# hide_st_style = """
#             <style>
#             .stDeployButton {display:none;}
#             footer {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)



def write_download_asset(b_size, name, download_url, download_count, button_type):
    mb_size = bytes_to_megabytes(b_size)
    st.subheader(f'**{name}**')
    st.link_button(f"**Download** ({mb_size} MB)", download_url, help = None, type = button_type, disabled=False, use_container_width=True)
    st.caption(f'Downloaded: **{download_count}** times')




def bytes_to_megabytes(bytes_size):
    megabytes = bytes_size / (1024 ** 2)
    rounded_megabytes = math.ceil(megabytes)
    return rounded_megabytes


def get_github_repo_assets_container(owner, repo_name, extension_filter):

    with st.container(border=True):

        with st.spinner(f'Getting the latest version of {repo_name}...'):
            time.sleep(0.5)

            repo_url = f"https://api.github.com/repos/{owner}/{repo_name}/releases/latest"


            headers = {
                "Accept": "application/vnd.github+json",
                
            } # "Authorization": f"Bearer {github_token}"
            
            response = requests.get(repo_url, headers=headers)

            if response.status_code == 200:
                ###########################################################################
                release_info = response.json()
                #print("From repo:", repo_url)
                #st.write("Release date:", release_info["published_at"])

                ###########################################################################
                release_date= release_info["published_at"]
                release_date_parsed = datetime.strptime(release_date, '%Y-%m-%dT%H:%M:%SZ')
                time_difference = datetime.utcnow() - release_date_parsed

                minutes = time_difference.total_seconds() // 60
                hours = time_difference.total_seconds() // 3600
                days = time_difference.days
                #weeks = math.ceil(time_difference.days / 7)
                weeks = time_difference.days / 7
                months = time_difference.days // 30.44

                seconds_in_a_year = 365.25 * 24 * 60 * 60
                years = int(time_difference.total_seconds() / seconds_in_a_year)
                #st.write(years)

                if years > 0:
                    ago = "years ago"
                    time_num = years
                elif months > 0:
                    ago = "months ago"
                    time_num = months
                elif weeks >= 1:
                    ago = "weeks ago"
                    time_num = math.ceil(weeks)
                elif days > 0:
                    ago = "days ago"
                    time_num = days
                elif hours > 0 : 
                    ago = "hours ago"
                    time_num = hours
                elif hours >= 0 : 
                    ago = "minutes ago"
                    time_num = minutes
                ###########################################################################
                
                #with st.container(border=True):
                    
                extension_filter = f".{extension_filter}"

                assets = release_info["assets"] 

                filtered_assets = []
                other_assets = []

                if assets:
                    for asset in assets:
                        if extension_filter in asset["name"]:
                            filtered_assets.append(asset)
                        else:
                            other_assets.append(asset)



                st.subheader(f"**{repo_name}**\nUpdated **{int(time_num)}** {ago}", divider = 'grey') # 'grey'

                #st.write(f"Updated **{days}** {ago}")
                # st.divider()

                #st.subheader("", divider='gray')


                tab1, tab2, tab3 = st.tabs([f"Main Assets ({len(filtered_assets)})", f"Other Assets ({len(other_assets)})", "Changelog"])

                
                with tab1:
                    if filtered_assets:
                        for asset in filtered_assets:
                                write_download_asset(asset["size"], asset["name"], asset["browser_download_url"], asset["download_count"], "primary")


                    else:
                        st.error("No assets found.")


                with tab2:
                    if other_assets:
                        for asset in other_assets:
                            write_download_asset(asset["size"], asset["name"], asset["browser_download_url"], asset["download_count"], "secondary")


                    else:
                        st.error("No assets found.")



                with tab3:
                    st.write(release_info["body"])



                return 0



            else:
                st.error(f"Failed to fetch release information of **{repo_name}**. Status code: [**{response.status_code}**]({repo_url})")

                #st.toast('The request limit from this IP address has been exceeded, please come back later', icon=None)


                #error_info = response.json()
                #with st.expander("Details", expanded=False) :
                    #st.write(error_info["message"])

                return 403 # 403



st.sidebar.title(f'Sidebar')

#all_ext = st.sidebar.toggle(f'Show all file extensions', value = False)


st.title("Github Assets Downloader")


####################################################################################
# col1, col2, col3 = st.columns(3)
# with col1:
#     owner, repo_name, extension_filter = "NoName-exe", "revanced-extended", "apk"
#     get_github_repo_assets_container(owner, repo_name, extension_filter)

# with col2:
#     owner, repo_name, extension_filter = "Team-xManager", "xManager", "apk"
#     get_github_repo_assets_container(owner, repo_name, extension_filter)

# with col3:
#     owner, repo_name, extension_filter = "NeoApplications", "Neo-Store", "apk"
#     get_github_repo_assets_container(owner, repo_name, extension_filter)
####################################################################################

statbox = []

owner, repo_name, extension_filter = "NoName-exe", "revanced-extended", "apk"
stat = get_github_repo_assets_container(owner, repo_name, extension_filter)
statbox.append(stat)

owner, repo_name, extension_filter = "Team-xManager", "xManager", "apk"
stat = get_github_repo_assets_container(owner, repo_name, extension_filter)
statbox.append(stat)

owner, repo_name, extension_filter = "vfsfitvnm", "ViMusic", "apk"
stat = get_github_repo_assets_container(owner, repo_name, extension_filter)
statbox.append(stat)

owner, repo_name, extension_filter = "NeoApplications", "Neo-Store", "apk"
stat = get_github_repo_assets_container(owner, repo_name, extension_filter)
statbox.append(stat)

error_403 = False

for stat in statbox:
    if stat == 403:
        error_403 = True

if error_403:
    st.toast('The request limit from this IP address has been exceeded, please come back later', icon=None)
