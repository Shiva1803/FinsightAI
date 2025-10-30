import axios from 'axios'
import type { ParsedDocument, VerificationResult, Record } from '../types'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const uploadDocument = async (file: File): Promise<{ id: number; parsed: ParsedDocument }> => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await api.post('/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

export const verifyDocuments = async (
  poFile?: File,
  invoiceFile?: File,
  poText?: string,
  invoiceText?: string
): Promise<VerificationResult> => {
  const formData = new FormData()
  
  if (poFile) formData.append('po_file', poFile)
  if (invoiceFile) formData.append('invoice_file', invoiceFile)
  if (poText) formData.append('po_text', poText)
  if (invoiceText) formData.append('invoice_text', invoiceText)
  
  const response = await api.post('/verify/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

export const verifyParsedDocuments = async (
  poData: ParsedDocument,
  invoiceData: ParsedDocument
): Promise<VerificationResult> => {
  const response = await api.post('/verify/parsed/', {
    po_data: poData,
    invoice_data: invoiceData,
  })
  return response.data
}

export const extractWithShivaay = async (
  file?: File,
  ocrText?: string
): Promise<ParsedDocument> => {
  const formData = new FormData()
  
  if (file) formData.append('file', file)
  if (ocrText) formData.append('ocr_text', ocrText)
  
  const response = await api.post('/extract/shivaay/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

export const getRecords = async (): Promise<Record[]> => {
  const response = await api.get('/records/')
  return response.data
}

export const deleteRecord = async (recordId: number): Promise<void> => {
  await api.delete(`/records/${recordId}`)
}

export const exportCSV = async (): Promise<Blob> => {
  const response = await api.get('/export/', {
    responseType: 'blob',
  })
  return response.data
}

export const healthCheck = async (): Promise<{ status: string }> => {
  const response = await api.get('/health/')
  return response.data
}
