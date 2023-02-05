FROM  python:3.8

RUN pip3 install --upgrade pip
RUN pip3 install ipykernel
RUN pip3 install carla==0.9.14

RUN pip3 install shapely networkx

WORKDIR /app/src

ENTRYPOINT ["python3","basic_agent.py"]
