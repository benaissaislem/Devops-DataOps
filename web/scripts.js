async function loadJSON(path) {
    const response = await fetch(path);
    return await response.json();
}

async function main() {
    // 1. Montant total par année (en M€ pour une meilleure lecture)
    const parAnnee = await loadJSON("data/montant_par_annee.json");
    new Chart(document.getElementById("chartAnnee"), {
        type: "bar",
        data: {
            labels: parAnnee.map(e => e.annee),
            datasets: [{
                label: "Montant total (M€)",
                data: parAnnee.map(e => e.montant / 1_000_000)
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: (value) => value.toLocaleString("fr-FR") + " M€"
                    }
                }
            }
        }
    });

    // 2. Nombre de marchés par année
    const nbParAnnee = await loadJSON("data/nb_marches_par_annee.json");
    new Chart(document.getElementById("chartNbMarches"), {
        type: "bar",
        data: {
            labels: nbParAnnee.map(e => e.annee),
            datasets: [{
                label: "Nombre de marchés",
                data: nbParAnnee.map(e => e.nb_marches)
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });

    // 3. Montant par nature de marché
    const parNature = await loadJSON("data/montant_par_nature.json");
    new Chart(document.getElementById("chartNature"), {
        type: "pie",
        data: {
            labels: parNature.map(e => e.nature),
            datasets: [{
                data: parNature.map(e => e.montant)
            }]
        }
    });

    // 4. Top 10 fournisseurs
    const topFour = await loadJSON("data/top_fournisseurs.json");
    new Chart(document.getElementById("chartFournisseurs"), {
        type: "bar",
        data: {
            labels: topFour.map(e => e.fournisseur),
            datasets: [{
                label: "Montant (M€)",
                data: topFour.map(e => e.montant / 1_000_000)
            }]
        },
        options: {
            indexAxis: "y",
            scales: {
                x: {
                    ticks: {
                        callback: (value) => value.toLocaleString("fr-FR") + " M€"
                    }
                }
            }
        }
    });

    // 5. Montant par périmètre financier
    const parPerimetre = await loadJSON("data/montant_par_perimetre.json");
    new Chart(document.getElementById("chartPerimetre"), {
        type: "bar",
        data: {
            labels: parPerimetre.map(e => e.perimetre),
            datasets: [{
                label: "Montant (M€)",
                data: parPerimetre.map(e => e.montant / 1_000_000)
            }]
        },
        options: {
            indexAxis: "y",
            scales: {
                x: {
                    ticks: {
                        callback: (value) => value.toLocaleString("fr-FR") + " M€"
                    }
                }
            }
        }
    });
}

main();
