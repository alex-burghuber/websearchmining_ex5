import org.json.JSONArray
import org.json.JSONObject
import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import org.jsoup.nodes.Element
import org.jsoup.select.Elements
import java.io.IOException

const val CS_PROFESSORS_URL = "http://informatik.jku.at/research/faculty.phtml"

data class Professor(
    val name: String,
    val position: String,
    val phone: String,
    val email: String,
    val room: String,
    val photoUrl: String
)

fun main() {
    val profs = scrapeJkuCsProfs()
    val jsonObjects = profs.map { prof ->
        JSONObject().put("name", prof.name)
            .put("position", prof.position)
            .put("phone", prof.phone)
            .put("email", prof.email)
            .put("room", prof.room)
            .put("photoUrl", prof.photoUrl)
    }
    val jsonArray = JSONArray(jsonObjects)
    println(jsonArray)
}

fun scrapeJkuCsProfs(): List<Professor> {
    println("Scraping JKU CS professors...")

    try {
        val doc: Document = Jsoup.connect(CS_PROFESSORS_URL).get()
        val profResultSets: Elements = doc.select("div.team_employee")

        return profResultSets.mapNotNull { profElement ->
            val infoP: Element? = profElement.nextElementSibling()
            if (infoP != null) {
                val name = infoP.select("em").text()

                val infos: List<String> = infoP.children()
                    .flatMap { it.textNodes() }
                    .mapNotNull { it.text().trim() }
                    .filter { it.isNotEmpty() }

                Professor(
                    name = name,
                    position = infos[0],
                    phone = infos[3 + infos.size - 5],
                    email = infos[4 + infos.size - 5],
                    room = infos[2 + infos.size - 5],
                    photoUrl = ""
                )
            } else {
                null
            }
        }

    } catch (e: IOException) {
        e.printStackTrace()
    }

    return emptyList()
}
