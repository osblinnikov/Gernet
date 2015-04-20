<%import parsing_java
p = reload(parsing_java)
p.parsingGernet(a)
dependenciesDict = dict()
for v in a.read_data["topology"]+a.read_data["depends"]:
  dependenciesDict[v["path"]] = v

%>

        %for k,v in dependenciesDict.items():
        <dependency>
            <groupId>${p.groupId(v["path"])}</groupId>
            <artifactId>${p.artifactId(v["path"])}</artifactId>
            <version>[0.0.0,)</version>
            <scope>compile</scope>
            %if v.has_key("type") and v["type"]=="apklib":
            <type>apklib</type>
            %endif
        </dependency>
        %endfor