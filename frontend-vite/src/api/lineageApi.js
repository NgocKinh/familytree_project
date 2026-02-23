// src/api/lineageApi.js
import axios from "axios";
import { API_BASE_URL } from "./apiConfig";

const LINEAGE_URL = `${API_BASE_URL}/lineage`;

// GET all
export const getAllLineages = () => axios.get(`${LINEAGE_URL}/`);

// GET by ID
export const getLineageById = (id) => axios.get(`${LINEAGE_URL}/${id}`);

// POST
export const createLineage = (lineageData) => axios.post(`${LINEAGE_URL}/`, lineageData);

// PUT
export const updateLineage = (id, lineageData) => axios.put(`${LINEAGE_URL}/${id}`, lineageData);

// DELETE
export const deleteLineage = (id) => axios.delete(`${LINEAGE_URL}/${id}`);



