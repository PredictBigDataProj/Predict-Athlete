const LeagueVisualizer = {
  selectors: {
    dataTable: "#data-table tbody tr",
    nationalityChart: "#nationality-chart",
    averageAge: "#average-age",
    ageStatsContainer: ".age-stats-container",
    positionData: ".position-data",
    positionAgeHeatmap: "#position-age-heatmap",
    agePyramidChart: "#age-pyramid-chart",
    positionSelect: "#position-select",
  },

  chartConfig: {
    nationality: {
      margin: { top: 30, right: 30, bottom: 70, left: 120 },
      width: 650,
      height: 300,
      colors: ["#4682B4", "#6A5ACD", "#20B2AA", "#FF6347", "#32CD32"],
    },
    heatmap: {
      margin: { top: 30, right: 30, bottom: 100, left: 100 },
      width: 470,
      height: 300,
    },
    pyramid: {
      margin: { top: 40, right: 80, bottom: 60, left: 80 },
      width: 540,
      height: 400,
    },
  },

  init: function () {
    document.addEventListener("DOMContentLoaded", () => {
      this.createNationalityChart();
      this.initAgeAnimation();
      this.createPositionAgeHeatmap();
      this.initAgePyramidChart();
    });
  },

  createNationalityChart: function () {
    const tableRows = document.querySelectorAll(this.selectors.dataTable);
    if (!tableRows.length) return;

    const nationData = {};
    tableRows.forEach((row) => {
      const nation = row.cells[3].textContent.trim();
      if (nation) {
        nationData[nation] = (nationData[nation] || 0) + 1;
      }
    });

    const data = Object.entries(nationData)
      .map(([nation, count]) => ({ nation, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 5);

    if (!data.length) return;

    const { margin, width, height, colors } = this.chartConfig.nationality;
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height;

    const svg = d3
      .select(this.selectors.nationalityChart)
      .append("svg")
      .attr("width", chartWidth + margin.left + margin.right)
      .attr("height", chartHeight + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    const x = d3
      .scaleLinear()
      .domain([0, d3.max(data, (d) => d.count)])
      .range([0, chartWidth]);

    const y = d3
      .scaleBand()
      .domain(data.map((d) => d.nation))
      .range([0, chartHeight])
      .padding(0.3);

    svg
      .append("g")
      .attr("class", "axis")
      .attr("transform", `translate(0,${chartHeight})`)
      .call(d3.axisBottom(x).ticks(5))
      .selectAll("text")
      .style("text-anchor", "end");

    svg.append("g").attr("class", "axis").call(d3.axisLeft(y));

    svg
      .append("text")
      .attr("class", "axis-label")
      .attr("x", chartWidth / 2)
      .attr("y", chartHeight + margin.bottom - 10)
      .style("text-anchor", "middle")
      .text("Number of Players");

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
      .on("mouseout", function () {
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
  },

  initAgeAnimation: function () {
    const ageElement = document.getElementById(
      this.selectors.averageAge.substring(1)
    );
    if (!ageElement) return;

    const targetAge = parseFloat(ageElement.textContent);
    const displayValue = ageElement.textContent;
    ageElement.textContent = "0";

    anime({
      targets: this.selectors.averageAge,
      innerHTML: [0, targetAge],
      easing: "easeInOutExpo",
      duration: 2000,
      delay: 500,
      update: function (anim) {
        const progress = anim.progress / 100;
        const currentValue = targetAge * progress;
        document.querySelector(
          LeagueVisualizer.selectors.averageAge
        ).innerHTML = currentValue.toFixed(2);
      },
      complete: function () {
        document.querySelector(
          LeagueVisualizer.selectors.averageAge
        ).innerHTML = displayValue;
      },
    });

    anime({
      targets: LeagueVisualizer.selectors.ageStatsContainer,
      translateY: [50, 0],
      opacity: [0, 1],
      easing: "easeOutElastic(1, .5)",
      duration: 1500,
      delay: 300,
    });
  },

  createPositionAgeHeatmap: function () {
    const positionData = document.querySelectorAll(this.selectors.positionData);
    if (!positionData.length) return;

    const heatmapData = [];
    const positions = [];
    const ageGroups = new Set();

    positionData.forEach((position) => {
      const posName = position.dataset.position;
      positions.push(posName);

      const ageGroupData = position.querySelectorAll(".age-group-data");
      ageGroupData.forEach((group) => {
        const groupName = group.dataset.group;
        const percent = parseFloat(group.dataset.percent);
        ageGroups.add(groupName);

        heatmapData.push({
          position: posName,
          ageGroup: groupName,
          value: percent,
        });
      });
    });

    const sortedAgeGroups = Array.from(ageGroups).sort();

    const { margin, width, height } = this.chartConfig.heatmap;
    const chartWidth = width;
    const chartHeight = height;

    const svg = d3
      .select(this.selectors.positionAgeHeatmap)
      .append("svg")
      .attr("width", chartWidth + margin.left + margin.right)
      .attr("height", chartHeight + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    const x = d3
      .scaleBand()
      .range([0, chartWidth])
      .domain(sortedAgeGroups)
      .padding(0.05);

    const y = d3
      .scaleBand()
      .range([chartHeight, 0])
      .domain(positions)
      .padding(0.05);

    svg
      .append("g")
      .attr("transform", `translate(0,${chartHeight})`)
      .call(d3.axisBottom(x))
      .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", ".15em")
      .attr("transform", "rotate(-65)");

    svg.append("g").call(d3.axisLeft(y));

    const colorScale = d3
      .scaleSequential()
      .interpolator(d3.interpolateBlues)
      .domain([0, d3.max(heatmapData, (d) => d.value)]);

    const tooltip = d3
      .select("body")
      .append("div")
      .style("position", "absolute")
      .style("background-color", "white")
      .style("border", "solid")
      .style("border-width", "1px")
      .style("border-radius", "5px")
      .style("padding", "10px")
      .style("opacity", 0);

    svg
      .selectAll()
      .data(heatmapData)
      .enter()
      .append("rect")
      .attr("x", (d) => x(d.ageGroup))
      .attr("y", (d) => y(d.position))
      .attr("width", x.bandwidth())
      .attr("height", y.bandwidth())
      .style("fill", (d) => colorScale(d.value))
      .on("mouseover", function (event, d) {
        tooltip.transition().duration(200).style("opacity", 0.9);
        tooltip
          .html(
            `Position: ${d.position}<br>Age Group: ${
              d.ageGroup
            }<br>Percentage: ${d.value.toFixed(2)}%`
          )
          .style("left", event.pageX + 10 + "px")
          .style("top", event.pageY - 28 + "px");
      })
      .on("mouseout", function () {
        tooltip.transition().duration(500).style("opacity", 0);
      });

    svg
      .append("text")
      .attr("x", chartWidth / 2)
      .attr("y", -10)
      .attr("text-anchor", "middle")
      .style("font-size", "16px")
      .text("Age Group Distribution by Position (%)");
  },

  initAgePyramidChart: function () {
    const positionSelect = document.getElementById(
      this.selectors.positionSelect.substring(1)
    );
    if (positionSelect) {
      positionSelect.addEventListener("change", function () {
        LeagueVisualizer.updateAgePyramidChart(this.value);
      });
    }

    this.createAgePyramidChart();
  },

  createAgePyramidChart: function () {
    const positionData = document.querySelectorAll(this.selectors.positionData);
    if (!positionData.length) return;

    const allPositionsData = {};
    const positionNames = [];

    positionData.forEach((position) => {
      const posName = position.dataset.position;
      positionNames.push(posName);

      const ageGroupData = position.querySelectorAll(".age-group-data");
      const posData = {};

      ageGroupData.forEach((group) => {
        const groupName = group.dataset.group;
        const percent = parseFloat(group.dataset.percent);
        posData[groupName] = percent;
      });

      allPositionsData[posName] = posData;
    });

    allPositionsData["all"] = this.combineAllPositionsData(
      allPositionsData,
      positionNames
    );

    this.renderPyramidChart(allPositionsData["all"], "all");
  },

  combineAllPositionsData: function (allPositionsData, positionNames) {
    const combinedData = {};
    const ageGroups = new Set();

    positionNames.forEach((pos) => {
      Object.keys(allPositionsData[pos]).forEach((group) => {
        ageGroups.add(group);
      });
    });

    ageGroups.forEach((group) => {
      let sum = 0;
      let count = 0;

      positionNames.forEach((pos) => {
        if (allPositionsData[pos][group] !== undefined) {
          sum += allPositionsData[pos][group];
          count++;
        }
      });

      combinedData[group] = count > 0 ? sum / count : 0;
    });

    return combinedData;
  },

  updateAgePyramidChart: function (position) {
    const positionData = document.querySelectorAll(this.selectors.positionData);
    if (!positionData.length) return;

    const allPositionsData = {};
    const positionNames = [];

    positionData.forEach((pos) => {
      const posName = pos.dataset.position;
      positionNames.push(posName);

      const ageGroupData = pos.querySelectorAll(".age-group-data");
      const posData = {};

      ageGroupData.forEach((group) => {
        const groupName = group.dataset.group;
        const percent = parseFloat(group.dataset.percent);
        posData[groupName] = percent;
      });

      allPositionsData[posName] = posData;
    });

    allPositionsData["all"] = this.combineAllPositionsData(
      allPositionsData,
      positionNames
    );

    const selectedData =
      position === "all"
        ? allPositionsData["all"]
        : allPositionsData[position] || allPositionsData["all"];

    this.renderPyramidChart(selectedData, position);
  },

  renderPyramidChart: function (data, position) {
    d3.select(this.selectors.agePyramidChart).html("");

    const ageGroups = Object.keys(data).sort((a, b) => {
      const aStart = parseInt(a.split("-")[0]);
      const bStart = parseInt(b.split("-")[0]);
      return aStart - bStart;
    });

    const { margin, width, height } = this.chartConfig.pyramid;
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;

    const svg = d3
      .select(this.selectors.agePyramidChart)
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    svg
      .append("text")
      .attr("class", "pyramid-title")
      .attr("x", chartWidth / 2)
      .attr("y", -20)
      .text(
        `Age Distribution for ${
          position === "all" ? "All Positions" : position
        }`
      );

    const y = d3
      .scaleBand()
      .domain(ageGroups)
      .range([0, chartHeight])
      .padding(0.1);

    const x = d3
      .scaleLinear()
      .domain([0, d3.max(Object.values(data)) * 1.1])
      .range([0, chartWidth / 2]);

    const tooltip = d3
      .select("body")
      .append("div")
      .attr("class", "pyramid-tooltip")
      .style("opacity", 0);

    svg
      .append("line")
      .attr("x1", chartWidth / 2)
      .attr("x2", chartWidth / 2)
      .attr("y1", 0)
      .attr("y2", chartHeight)
      .style("stroke", "#999")
      .style("stroke-dasharray", "4,4");

    svg
      .append("g")
      .attr("class", "pyramid-axis")
      .attr("transform", `translate(${chartWidth / 2},0)`)
      .call(d3.axisLeft(y).tickSize(0))
      .selectAll(".domain")
      .remove();

    svg
      .append("text")
      .attr("class", "pyramid-label")
      .attr("x", chartWidth / 4)
      .attr("y", chartHeight + 40)
      .text("Younger Age Groups");

    svg
      .append("text")
      .attr("class", "pyramid-label")
      .attr("x", (3 * chartWidth) / 4)
      .attr("y", chartHeight + 40)
      .text("Older Age Groups");

    const youngerGroups = ageGroups.slice(0, Math.ceil(ageGroups.length / 2));
    const olderGroups = ageGroups.slice(Math.ceil(ageGroups.length / 2));

    this.createPyramidBars(
      svg,
      youngerGroups,
      data,
      x,
      y,
      chartWidth,
      tooltip,
      "left"
    );

    this.createPyramidBars(
      svg,
      olderGroups,
      data,
      x,
      y,
      chartWidth,
      tooltip,
      "right"
    );
  },

  createPyramidBars: function (svg, groups, data, x, y, width, tooltip, side) {
    const isLeft = side === "left";

    svg
      .selectAll(`.pyramid-bar-${side}`)
      .data(groups)
      .enter()
      .append("rect")
      .attr("class", `pyramid-bar-${side}`)
      .attr("x", isLeft ? width / 2 - x(0) : width / 2)
      .attr("y", (d) => y(d))
      .attr("width", 0)
      .attr("height", y.bandwidth())
      .on("mouseover", function (event, d) {
        tooltip.transition().duration(200).style("opacity", 0.9);
        tooltip
          .html(`Age Group: ${d}<br>Percentage: ${data[d].toFixed(2)}%`)
          .style("left", event.pageX + 10 + "px")
          .style("top", event.pageY - 28 + "px");
      })
      .on("mouseout", function () {
        tooltip.transition().duration(500).style("opacity", 0);
      })
      .transition()
      .duration(1000)
      .attr("x", (d) => (isLeft ? width / 2 - x(data[d]) : width / 2))
      .attr("width", (d) => x(data[d]));

    svg
      .selectAll(`.${side}-label`)
      .data(groups)
      .enter()
      .append("text")
      .attr("class", `${side}-label`)
      .attr("x", (d) =>
        isLeft ? width / 2 - x(data[d]) - 5 : width / 2 + x(data[d]) + 5
      )
      .attr("y", (d) => y(d) + y.bandwidth() / 2)
      .attr("dy", ".35em")
      .attr("text-anchor", isLeft ? "end" : "start")
      .style("font-size", "12px")
      .style("opacity", 0)
      .text((d) => `${data[d].toFixed(1)}%`)
      .transition()
      .delay(1000)
      .duration(500)
      .style("opacity", 1);
  },
};

LeagueVisualizer.init();
