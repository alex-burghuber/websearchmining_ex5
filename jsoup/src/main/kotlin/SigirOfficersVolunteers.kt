import org.json.JSONArray
import org.json.JSONObject
import org.jsoup.Jsoup

const val SIGIR_TEAM_MEMBERS_URL = "https://sigir.org/general-information/officers-and-volunteers/"

data class SigirTeamMember(val name: String, val position: String, val email: String)

fun main() {
    val teamMembers = sigirOfficersVolunteers()

    val jsonObjects = teamMembers.map { member ->
        JSONObject().put("name", member.name)
            .put("position", member.position)
            .put("email", member.email)
    }
    val jsonArray = JSONArray(jsonObjects)
    println(jsonArray)
}

fun sigirOfficersVolunteers(): List<SigirTeamMember> {
    println("Scraping Sigir team members...")

    val doc = Jsoup.connect(SIGIR_TEAM_MEMBERS_URL).get()

    val memberPList = doc.select("div.entry-content").first()?.select("p") ?: return emptyList()

    val members = mutableListOf<SigirTeamMember>()

    for (memberP in memberPList) {
        val name = memberP.selectFirst("a")?.text() ?: ""
        val position = memberP.selectFirst("strong")?.text() ?: ""
        val email = memberP.textNodes().find { it.text().contains("@") }?.text()?.trim() ?: ""
        members.add(SigirTeamMember(name, position, email))
    }

    return members
}
