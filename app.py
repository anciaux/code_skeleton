import streamlit as st
import subprocess
import base64
import tempfile
import os

st.set_page_config(layout="wide")

st.markdown('# Class hierarchy UML generator')
text = st.text_area('Insert your class hierarchy here', value='''
class Animal
  public pure virtual void scream();
  public std::string & getName(); 
  public void setName(std::string & toto);
  protected std::string name;

class Cat(Animal)
  public virtual void scream();

class Dog(Animal)
  public virtual void scream();
''', height=500)


def generate_class_diag(collab=False, inheritance=True):

    with tempfile.NamedTemporaryFile(mode='w') as f:
        f.write(text)
        f.flush()

        fname = f.name
        opt = ''
        if not collab:
            opt += ' --collaboration_no'
        if not inheritance:
            opt += ' --inheritance_no'
        p = subprocess.run(
            f'class_dumper_dot {opt} -c {fname} -f svg -o {fname}.svg',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        try:
            p.check_returncode()
        except subprocess.CalledProcessError as e:
            st.error("failed launching class_dumper_dot")
            if e.stderr:
                st.error(f"{e.stderr.decode()}")
                return

        p = subprocess.run(
            f'class_dumper_dot {opt} -c {fname} -f pdf -o {fname}.pdf',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        try:
            p.check_returncode()
        except subprocess.CalledProcessError as e:
            st.error("failed launching class_dumper_dot")
            if e.stderr:
                st.error(f"{e.stderr.decode()}")
                return

        with open(f'{fname}.svg', 'rb') as f:
            b64_svg = base64.b64encode(f.read()).decode("utf-8")
        with open(f'{fname}.pdf', 'rb') as f:
            pdf = f.read()
        with open(f'{fname}.svg', 'rb') as f:
            svg = f.read()
        os.remove(f'{fname}.svg')
        os.remove(f'{fname}.dot')
        os.remove(f'{fname}.pdf')
        return svg, pdf, b64_svg


col1, col2, col3 = st.columns(3)

collab = col2.checkbox("Show Collaborations", value=False)
inheritance = col1.checkbox("Show Inheritance", value=True)

svg, pdf, b64_svg = generate_class_diag(collab, inheritance)
col1, col2, col3 = st.columns(3)

col1.download_button('Download as PDF', data=pdf,
                     file_name='uml.pdf', use_container_width=True)
col2.download_button('Download as SVG', data=svg,
                     file_name='uml.svg', use_container_width=True)
col3.download_button('Download as classes', data=text,
                     file_name='uml.classes', use_container_width=True)

zoom = st.slider("Zoom level", value=50, min_value=1, max_value=100)


html = r'<center><img src="data:image/svg+xml;base64,%s" ' % b64_svg
html += f'width="{zoom}%"/></center>'
st.write(html, unsafe_allow_html=True)
