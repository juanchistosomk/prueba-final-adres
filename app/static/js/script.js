document.addEventListener("DOMContentLoaded", () => {
  const searchForm = document.getElementById("searchForm");

  if (document.getElementById("resultadosTabla")) {
    listarDatos();
  }

  if (document.getElementById("historialTabla")) {
    cargarHistorial();
  }

  // Validación del formulario de creación de adquisición
  const creationForm = document.getElementById("creationForm");
  if (creationForm) {
    // Calcular valor total automáticamente
    const cantidad = document.getElementById("cantidad");
    const valorUnitario = document.getElementById("valorUnitario");
    const valorTotal = document.getElementById("valorTotal");

    function calcularTotal() {
      if (cantidad.value && valorUnitario.value) {
        valorTotal.value = (
          Number.parseFloat(cantidad.value) *
          Number.parseFloat(valorUnitario.value)
        ).toFixed(0);
      } else {
        valorTotal.value = "";
      }
    }

    cantidad.addEventListener("input", calcularTotal);
    valorUnitario.addEventListener("input", calcularTotal);

    // Validación del formulario adquisición
    creationForm.addEventListener("submit", (event) => {
      if (!creationForm.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      } else {
        event.preventDefault();
        creationForm.submit();
      }
      creationForm.classList.add("was-validated");
    });
  }

  // Formulario de búsqueda

  if (searchForm) {
    searchForm.addEventListener("submit", (event) => {
      event.preventDefault();
      listarDatos();
    });
  }

  async function listarDatos() {
    const response = await fetch(
      "http://127.0.0.1:5000/api/v1/adquisiciones/list-one",
      { method: "POST", body: new FormData(searchForm) }
    );
    const datos = await response.json();
    //console.log("datos: ", datos);

    const tabla = document.getElementById("resultadosTabla");
    tabla.innerHTML = "";

    if (datos.length === 0) {
      const fila = document.createElement("tr");
      fila.innerHTML = `<td colspan="10" class="text-center">No se encontraron resultados</td>`;
      tabla.appendChild(fila);
      return;
    }

    datos.forEach((item) => {
      const fila = document.createElement("tr");
      fila.innerHTML = `
            <td>${formatearMoneda(item.presupuesto)}</td>
            <td>${item.unidad}</td>
            <td>${item.tipo}</td>
            <td>${item.cantidad}</td>
            <td>${formatearMoneda(item.valor_unitario)}</td>
            <td>${formatearMoneda(item.valor_total)}</td>
            <td>${formatearFecha(item.fecha_adquisicion)}</td>
            <td>${item.proveedor}</td>
            <td>${item.documentacion}</td>
            <td class="d-flex justify-content-between align-items-center">
                <a class="btn btn-sm btn-info me-1" href="/editar-adquisicion/${
                  item.id
                }"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
  <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
  <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
</svg></a>
                <button class="btn btn-sm btn-danger" onclick="desactivarItem(
                  ${item.id}
                )"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-power" viewBox="0 0 16 16">
  <path d="M7.5 1v7h1V1z"/>
  <path d="M3 8.812a5 5 0 0 1 2.578-4.375l-.485-.874A6 6 0 1 0 11 3.616l-.501.865A5 5 0 1 1 3 8.812"/>
</svg></button>
            </td>
        `;
      tabla.appendChild(fila);
    });
  }

  // Cargar datos del historial
  async function cargarHistorial() {
    const response = await fetch(
      "http://127.0.0.1:5000/api/v1/historial/list",
      { method: "GET" }
    );
    const historial = await response.json();

    const tabla = document.getElementById("historialTabla");
    tabla.innerHTML = "";

    historial.forEach((item) => {
      const fila = document.createElement("tr");
      fila.innerHTML = `
            <td>${item.fecha_modificacion}</td>
            <td>${item.tipo_modificacion}</td>
             <td><B>#ID: ${item.id}</B><br>Presupuesto: $${item.presupuesto}<br>Cant: ${item.cantidad}<br>Valor_unit: $${item.valor_unitario}<br>Valor_total: $${item.valor_total}<br>Fecha adq.: ${item.fecha_adquisicion}<br>Proveedor: ${item.proveedor}<br>Tipo: ${item.tipo}<br>Unidad: ${item.unidad}<br>Estado: ${item.estado}<br></td>
            <td>${item.usuario_modificacion}</td>
        `;
      tabla.appendChild(fila);
    });
  }

  /********** Funciones de utilidad **********/

  function formatearMoneda(valor) {
    return new Intl.NumberFormat("es-CO", {
      style: "currency",
      currency: "COP",
      minimumFractionDigits: 0,
      maximumFractionDigits: 2,
    }).format(valor);
  }

  function formatearFecha(fecha) {
    return fecha; //new Date(fecha).toLocaleDateString("es-CO");
  }
});

async function desactivarItem(id) {
  if (confirm("¿⚠️Está seguro que desea desactivar el registro?")) {
    const response = await fetch(
      `http://127.0.0.1:5000/api/v1/adquisiciones/desactive/${id}`,
      { method: "GET" }
    );
    const desactiva = await response.json();

    alert(`${desactiva.message}`);
    location.reload();
  }
}
