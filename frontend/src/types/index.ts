export interface LineItem {
  description: string
  sku: string | null
  unit_price: number | null
  quantity: number | null
  line_total: number | null
}

export interface ParsedDocument {
  document_type: string
  vendor_name: string | null
  vendor_tax_id: string | null
  buyer_name: string | null
  buyer_tax_id: string | null
  document_number: string | null
  po_number: string | null
  invoice_date: string | null
  due_date: string | null
  currency: string | null
  total_amount: number | null
  subtotal_amount: number | null
  tax_amount: number | null
  line_items: LineItem[]
  footnotes: string | null
  raw_text_snippet: string
  extraction_warnings: string[]
  extraction_debug: Record<string, any>
}

export interface VerificationSummary {
  vendor_match: boolean
  po_number_match: boolean
  invoice_number_found: boolean
  total_match: boolean
  amount_difference: number
  tax_match: boolean
  currency_match: boolean
  date_difference_days: number | null
  discrepancy_level: 'none' | 'low' | 'medium' | 'high'
  po_confidence: number
  invoice_confidence: number
  validation_passed: boolean
  needs_review: boolean
}

export interface AnomalyInsights {
  anomaly_detected: boolean
  anomaly_types: string[]
  anomaly_reason: string
  pattern: string
  risk_score: number
  historical_trend: string
  fraud_indicators: string[]
}

export interface VisualizationData {
  bar_chart: {
    labels: string[]
    values: number[]
    currency: string
  }
  pie_chart: {
    discrepancy_breakdown: Record<string, number>
  }
  line_items_comparison: Array<{
    description: string
    po_qty: number | null
    invoice_qty: number | null
    po_price: number | null
    invoice_price: number | null
    qty_match: boolean
    price_match: boolean
    status?: string
  }>
  naughty_list_score: number
  timeline: {
    events: Array<{
      date: string
      event: string
      document: string
    }>
    total_days: number | null
  }
  discrepancy_count: number
  high_severity_count: number
}

export interface VerificationResult {
  verification_summary: VerificationSummary
  anomaly_insights: AnomalyInsights
  visualization_data: VisualizationData
  verified_by: string
  timestamp: string
  po_file: string
  invoice_file: string
}

export interface Record {
  id: number
  source_file: string
  parsed: ParsedDocument | VerificationResult
  record_type?: 'document' | 'verification'
}
