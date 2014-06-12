<%import parsing_java as p
p.parsingGernet(a)%>

        %for v in a.read_data["blocks"]+a.read_data["depends"]:
        <dependency>
            <groupId>${p.groupId(v["path"])}</groupId>
            <artifactId>${p.artifactId(v["path"])}</artifactId>
            <version>${v["ver"]}</version>
            <scope>compile</scope>
            %if v.has_key("type") and v["type"]=="apklib":
            <type>apklib</type>
            %endif
        </dependency>
        %endfor