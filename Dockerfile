FROM postgres

ARG ARG_VAR
RUN echo $ARG_VAR

COPY . .
RUN ["chmod", "+x", "./scripts.sh"]
ENV ARG_VAR ${ARG_VAR}
ENV NEW_ARG test
CMD ["./scripts.sh"]

# ENTRYPOINT ["sh", "./scripts.sh", "test"]
