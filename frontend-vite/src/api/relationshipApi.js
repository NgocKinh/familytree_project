// src/api/relationshipApi.js
import axios from "axios";
import { API_BASE_URL } from "./apiConfig";

const REL_URL = `${API_BASE_URL}/api/relationship`;

// GET all
export const getAllRelationships = () => axios.get(`${REL_URL}/`);

// GET by ID
export const getRelationshipById = (id) => axios.get(`${REL_URL}/${id}`);

// POST
export const createRelationship = (data) => axios.post(`${REL_URL}/`, data);

// PUT
export const updateRelationship = (id, data) => axios.put(`${REL_URL}/${id}`, data);

// DELETE
export const deleteRelationship = (id) => axios.delete(`${REL_URL}/${id}`);

// FIND RELATIONSHIP (ENGINE)
export const findRelationship = (fromId, toId) =>
  axios.post(`${REL_URL}/find`, {
    from_person_id: fromId,
    to_person_id: toId,
  });
