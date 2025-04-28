document.addEventListener("DOMContentLoaded", function () {
  const tableRows = document.querySelectorAll("#data-table tbody tr");
  const nationData = {};

  tableRows.forEach((row) => {
    const nation = row.cells[3].textContent.trim();
    if (nation) {
      nationData[nation] = (nationData[nation] || 0) + 1;
    }
  });

  const data = Object.entries(nationData)
    .map(([nation, count]) => ({
      nation,
      count,
    }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5);

  const margin = { top: 30, right: 30, bottom: 70, left: 120 };
  const width = 800 - margin.left - margin.right;
  const height = 300;

  const svg = d3
    .select("#nationality-chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const x = d3
    .scaleLinear()
    .domain([0, d3.max(data, (d) => d.count)])
    .range([0, width]);

  const y = d3
    .scaleBand()
    .domain(data.map((d) => d.nation))
    .range([0, height])
    .padding(0.3);

  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x).ticks(5))
    .selectAll("text")
    .style("text-anchor", "end");

  svg.append("g").attr("class", "axis").call(d3.axisLeft(y));

  svg
    .append("text")
    .attr("class", "axis-label")
    .attr("x", width / 2)
    .attr("y", height + margin.bottom - 10)
    .style("text-anchor", "middle")
    .text("Number of Players");

  const colors = ["#4682B4", "#6A5ACD", "#20B2AA", "#FF6347", "#32CD32"];

  svg
    .selectAll(".bar")
    .data(data)
    .enter()
    .append("rect")
    .attr("class", "bar")
    .attr("y", (d) => y(d.nation))
    .attr("height", y.bandwidth())
    .attr("x", 0)
    .attr("width", 0)
    .attr("fill", (d, i) => colors[i % colors.length])
    .on("mouseover", function (event, d) {
      d3.select(this).attr("opacity", 0.8);

      svg
        .append("text")
        .attr("class", "tooltip")
        .attr("x", x(d.count) + 5)
        .attr("y", y(d.nation) + y.bandwidth() / 2)
        .attr("dy", ".35em")
        .style("font-size", "12px")
        .text(`${d.count} players`);
    })
    .on("mouseout", function (event, d, i) {
      d3.select(this).attr("opacity", 1);
      svg.selectAll(".tooltip").remove();
    })
    .transition()
    .duration(800)
    .attr("width", (d) => x(d.count));

  svg
    .selectAll(".count-label")
    .data(data)
    .enter()
    .append("text")
    .attr("class", "count-label")
    .attr("x", (d) => x(d.count) - 10)
    .attr("y", (d) => y(d.nation) + y.bandwidth() / 2)
    .attr("dy", ".35em")
    .attr("text-anchor", "end")
    .style("font-size", "14px")
    .style("font-weight", "bold")
    .style("fill", "white")
    .style("opacity", 0)
    .text((d) => d.count)
    .transition()
    .delay(800)
    .duration(500)
    .style("opacity", 1);
});

document.addEventListener("DOMContentLoaded", function () {
  // Get the target value from the element
  const ageElement = document.getElementById("average-age");
  if (!ageElement) return;

  const targetAge = parseFloat(ageElement.textContent);
  // Store the target value for animation
  const displayValue = ageElement.textContent;
  // Reset to zero for animation
  ageElement.textContent = "0";

  // Set up the animation
  anime({
    targets: "#average-age",
    innerHTML: [0, targetAge],
    easing: "easeInOutExpo",
    duration: 2000,
    delay: 500,
    update: function (anim) {
      const progress = anim.progress / 100;
      const currentValue = targetAge * progress;
      document.querySelector("#average-age").innerHTML = currentValue.toFixed(2);
    },
    complete: function() {
      // Ensure the final value matches exactly what was provided by Flask
      document.querySelector("#average-age").innerHTML = displayValue;
    }
  });

  // Add entrance animation for the container
  anime({
    targets: ".age-stats-container",
    translateY: [50, 0],
    opacity: [0, 1],
    easing: "easeOutElastic(1, .5)",
    duration: 1500,
    delay: 300,
  });
});
