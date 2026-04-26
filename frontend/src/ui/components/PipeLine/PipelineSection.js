export function PipelineSection() {
  return `
    <section id="pipeline" class="tab-content">

      <div class="panel metrics">
        <div class="card">
          <h3>Total</h3>
          <div id="total">-</div>
        </div>

        <div class="card">
          <h3>Short</h3>
          <div id="short">-</div>
        </div>

        <div class="card">
          <h3>Latency</h3>
          <div id="latency">-</div>
        </div>
      </div>

      <div class="panel">
        <div id="results"></div>
      </div>

    </section>
  `
}