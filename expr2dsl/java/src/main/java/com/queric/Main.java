package com.queric;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.Arrays;
import java.util.List;

/**
 * Entry point: parse query and optionally write DSL JSON.
 */
public final class Main {

    private static final ObjectMapper JSON = new ObjectMapper()
        .enable(SerializationFeature.INDENT_OUTPUT);

    public static void main(String[] args) throws Exception {
        QueryParser parser = new QueryParser(Arrays.asList("title", "keywords", "abstract"));

//        String q = "((\"协同过滤\" AND \"推荐算法\")\n"
//            + "OR\n"
//            + "(\"协同过滤\" AND \"推荐系统\" AND 算法)\n"
//            + "OR\n"
//            + "(\"协同过滤算法\"))";

        // Or the full example:
         String q = "(( \"氢气浓度\" OR \"氢浓度\" OR \"浓度衰减\" OR \"衰减模型\"  AND \"膜湿度\" OR \"湿度\" OR \"加湿\" OR \"水含量\"  AND \"泄露率\" OR \"泄漏率\" OR \"渗透率\" OR \"实测\"  AND \"电堆\" OR \"燃料电池\" OR \"电堆寿命\" OR \"使用寿命\"  AND  (IPC:(H01M8) OR IPC:(H01M4)) ) AND ( APD:[20200101 TO 20251231] )) AND (燃料电池)";

        java.util.Map<String, Object> dsl = parser.parse(q);
        String out = JSON.writerWithDefaultPrettyPrinter().writeValueAsString(dsl);

        String userDir = System.getProperty("user.dir", ".");
        File cwd = new File(userDir);
        File outPath = "java".equals(cwd.getName())
            ? new File(cwd, "dsl.json")
            : new File(userDir, "dsl.json");
        Files.write(outPath.toPath(), out.getBytes(StandardCharsets.UTF_8));
        System.out.println("done");
    }
}
