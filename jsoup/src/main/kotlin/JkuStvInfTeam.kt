import org.json.JSONArray
import org.json.JSONObject
import org.jsoup.Jsoup
import org.jsoup.nodes.Document

const val STV_INF_URL = "https://new.oeh.jku.at/studium/tnf/informatik/team"

data class StvTeamMember(val name: String, val position: String)

fun main() {
    val teamMembers = scrapeJkuStvInfTeam()

    val jsonObjects = teamMembers.map { member ->
        JSONObject().put("name", member.name)
            .put("member", member.position)
    }
    val jsonArray = JSONArray(jsonObjects)
    println(jsonArray)
}

fun scrapeJkuStvInfTeam(): List<StvTeamMember> {
    println("Scraping JKU Stv Informatik team members...")

    val doc: Document = Jsoup.connect(STV_INF_URL).get()

    val potentialMembers = doc.select("div.section.section-separated")

    val members = mutableListOf<StvTeamMember>()

    for (potMember in potentialMembers) {
        val position = potMember.selectFirst("div.h6.mb-_5")?.text()
        val name = potMember.selectFirst("h2")?.text()

        members.add(StvTeamMember(name?.trim() ?: "", position?.trim() ?: ""))
    }

    return members
}

