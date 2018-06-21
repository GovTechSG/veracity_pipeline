FROM govtechsg/cicd-images:robot-selenium-latest
RUN apt-get update && apt-get -y install libpq-dev
RUN pip install psycopg2
CMD ["pybot", "-d", "./results/ror_test_01","-x", "xunit_output.xml","-A", "argfile.txt"]