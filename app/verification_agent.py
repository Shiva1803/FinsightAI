"""
Futurix AI Verification Agent
Advanced PO vs Invoice verification with anomaly detection and dashboard data generation
"""
import json
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from .extractor import parse_document, validate_po_invoice_match
from . import utils


class VerificationAgent:
    """AI-driven verification agent for PO vs Invoice comparison"""
    
    def __init__(self, vendor_history: Optional[Dict[str, Any]] = None):
        """
        Initialize verification agent
        
        Args:
            vendor_history: Historical anomaly data for vendors
        """
        self.vendor_history = vendor_history or {}
        self.confidence_threshold = 0.6
    
    def verify_documents(self, po_data: Dict[str, Any], invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main verification method - compares PO and Invoice
        
        Args:
            po_data: Dict with 'file_name' and 'extracted_text' or parsed data
            invoice_data: Dict with 'file_name' and 'extracted_text' or parsed data
        
        Returns:
            Complete verification result with summary, anomalies, and visualization data
        """
        # Handle both raw text and pre-parsed data
        if "extracted_text" in po_data:
            po_parsed = parse_document(po_data["extracted_text"])
            po_parsed["file_name"] = po_data.get("file_name", "unknown")
        else:
            po_parsed = po_data
        
        if "extracted_text" in invoice_data:
            invoice_parsed = parse_document(invoice_data["extracted_text"])
            invoice_parsed["file_name"] = invoice_data.get("file_name", "unknown")
        else:
            invoice_parsed = invoice_data
        
        # Perform validation
        validation = validate_po_invoice_match(po_parsed, invoice_parsed)
        
        # Build verification summary
        summary = self._build_verification_summary(po_parsed, invoice_parsed, validation)
        
        # Detect anomalies
        anomalies = self._detect_anomalies(po_parsed, invoice_parsed, validation, summary)
        
        # Generate visualization data
        viz_data = self._generate_visualization_data(po_parsed, invoice_parsed, validation, anomalies)
        
        # Build final response
        result = {
            "verification_summary": summary,
            "anomaly_insights": anomalies,
            "visualization_data": viz_data,
            "verified_by": "Futurix AI Verification Agent",
            "timestamp": datetime.utcnow().isoformat(),
            "po_file": po_parsed.get("file_name", "unknown"),
            "invoice_file": invoice_parsed.get("file_name", "unknown")
        }
        
        return result
    
    def _build_verification_summary(self, po: Dict, invoice: Dict, validation: Dict) -> Dict[str, Any]:
        """Build verification summary section"""
        
        # Vendor match
        vendor_match = False
        if po.get("vendor_name") and invoice.get("vendor_name"):
            vendor_match = utils.fuzzy_match(
                utils.normalize_name(po["vendor_name"]),
                utils.normalize_name(invoice["vendor_name"]),
                threshold=0.8
            )
        
        # PO number match
        po_number_match = False
        if invoice.get("po_number") and po.get("document_number"):
            po_number_match = invoice["po_number"].lower() == po["document_number"].lower()
        
        # Invoice number found
        invoice_number_found = invoice.get("document_number") is not None
        
        # Total match
        po_total = po.get("total_amount", 0) or 0
        inv_total = invoice.get("total_amount", 0) or 0
        amount_difference = abs(inv_total - po_total)
        total_match = amount_difference <= (po_total * 0.02) if po_total > 0 else False  # 2% tolerance
        
        # Tax match
        tax_match = True
        if po.get("tax_amount") and invoice.get("tax_amount"):
            tax_diff_pct = abs(po["tax_amount"] - invoice["tax_amount"]) / po["tax_amount"] * 100
            tax_match = tax_diff_pct <= 5.0  # 5% tolerance
        
        # Date difference
        date_difference_days = None
        if po.get("invoice_date") and invoice.get("invoice_date"):
            try:
                po_date = datetime.fromisoformat(po["invoice_date"])
                inv_date = datetime.fromisoformat(invoice["invoice_date"])
                date_difference_days = abs((inv_date - po_date).days)
            except:
                pass
        
        # Currency match
        currency_match = True
        if po.get("currency") and invoice.get("currency"):
            currency_match = po["currency"] == invoice["currency"]
        
        # Discrepancy level
        discrepancy_level = self._calculate_discrepancy_level(validation, amount_difference, po_total)
        
        # Confidence scores
        po_confidence = self._calculate_document_confidence(po)
        invoice_confidence = self._calculate_document_confidence(invoice)
        
        # Check if same document (no review needed)
        same_document = validation.get("match_method") == "same_document" and validation.get("match_score", 0) >= 1.0
        
        return {
            "vendor_match": vendor_match,
            "po_number_match": po_number_match,
            "invoice_number_found": invoice_number_found,
            "total_match": total_match,
            "amount_difference": round(amount_difference, 2),
            "tax_match": tax_match,
            "currency_match": currency_match,
            "date_difference_days": date_difference_days,
            "discrepancy_level": discrepancy_level,
            "po_confidence": round(po_confidence, 2),
            "invoice_confidence": round(invoice_confidence, 2),
            "validation_passed": validation["matched"] and validation["high_severity_count"] == 0,
            "needs_review": False if same_document else (validation["high_severity_count"] > 0 or po_confidence < 0.6 or invoice_confidence < 0.6)
        }
    
    def _calculate_discrepancy_level(self, validation: Dict, amount_diff: float, po_total: float) -> str:
        """Calculate overall discrepancy level"""
        # Check if documents matched perfectly (same document uploaded twice)
        if validation.get("match_method") == "same_document" and validation.get("match_score", 0) >= 1.0:
            return "none"
        
        high_severity = validation.get("high_severity_count", 0)
        
        if high_severity > 0:
            return "high"
        
        if po_total > 0:
            diff_pct = (amount_diff / po_total) * 100
            if diff_pct > 10:
                return "high"
            elif diff_pct > 5:
                return "medium"
        
        if validation.get("discrepancy_count", 0) > 2:
            return "medium"
        elif validation.get("discrepancy_count", 0) > 0:
            return "low"
        
        return "none"
    
    def _calculate_document_confidence(self, doc: Dict) -> float:
        """Calculate overall document extraction confidence"""
        scores = []
        
        # Check critical fields
        if doc.get("vendor_name"):
            scores.append(0.9)
        if doc.get("document_number"):
            scores.append(0.9)
        if doc.get("total_amount"):
            scores.append(0.95)
        if doc.get("invoice_date"):
            scores.append(0.85)
        if doc.get("line_items"):
            scores.append(0.8)
        
        # Penalize for warnings
        warning_count = len(doc.get("extraction_warnings", []))
        penalty = min(warning_count * 0.1, 0.3)
        
        avg_score = sum(scores) / len(scores) if scores else 0.3
        return max(avg_score - penalty, 0.0)
    
    def _detect_anomalies(self, po: Dict, invoice: Dict, validation: Dict, summary: Dict) -> Dict[str, Any]:
        """Detect anomalies and fraudulent patterns"""
        
        anomalies = []
        pattern_type = "normal"
        anomaly_reason = None
        
        # If same document uploaded twice, no anomalies
        if validation.get("match_method") == "same_document" and validation.get("match_score", 0) >= 1.0:
            return {
                "anomaly_detected": False,
                "anomaly_types": [],
                "anomaly_reason": "Documents match perfectly - same document uploaded twice",
                "pattern": "identical_documents",
                "risk_score": 0.0,
                "historical_trend": self._get_vendor_history(invoice.get("vendor_name", "Unknown")),
                "fraud_indicators": []
            }
        
        # Check for overbilling
        if summary["amount_difference"] > 0:
            po_total = po.get("total_amount", 0) or 0
            inv_total = invoice.get("total_amount", 0) or 0
            
            if inv_total > po_total:
                diff_pct = (summary["amount_difference"] / po_total * 100) if po_total > 0 else 0
                if diff_pct > 10:
                    pattern_type = "overbilling"
                    anomaly_reason = f"Invoice total higher than PO by ₹{summary['amount_difference']:.2f} ({diff_pct:.1f}%)"
                    anomalies.append("significant_overbilling")
                elif diff_pct > 5:
                    pattern_type = "possible_overbilling"
                    anomaly_reason = f"Invoice total exceeds PO by ₹{summary['amount_difference']:.2f} ({diff_pct:.1f}%)"
                    anomalies.append("moderate_overbilling")
        
        # Check for price manipulation
        for disc in validation.get("discrepancies", []):
            if disc["type"] == "price_mismatch":
                anomalies.append("price_manipulation")
                if not anomaly_reason:
                    anomaly_reason = disc["message"]
            elif disc["type"] == "quantity_mismatch":
                anomalies.append("quantity_discrepancy")
                if not anomaly_reason:
                    anomaly_reason = disc["message"]
        
        # Check for vendor mismatch (potential fraud)
        if not summary["vendor_match"]:
            anomalies.append("vendor_mismatch")
            pattern_type = "vendor_fraud_risk"
            anomaly_reason = f"Vendor name mismatch: PO='{po.get('vendor_name')}' vs Invoice='{invoice.get('vendor_name')}'"
        
        # Check for duplicate invoice
        if invoice.get("document_number"):
            # This would check against database in production
            # For now, just flag if confidence is low
            if summary["invoice_confidence"] < 0.5:
                anomalies.append("suspicious_document")
        
        # Check for tax rate anomalies
        if not summary["tax_match"]:
            anomalies.append("tax_discrepancy")
            if not anomaly_reason:
                anomaly_reason = "Tax amount mismatch between PO and Invoice"
        
        # Check for date anomalies
        if summary["date_difference_days"] and summary["date_difference_days"] > 60:
            anomalies.append("unusual_date_gap")
            if not anomaly_reason:
                anomaly_reason = f"Unusual date gap: {summary['date_difference_days']} days between PO and Invoice"
        
        # Get vendor history
        vendor_name = invoice.get("vendor_name", "Unknown")
        historical_trend = self._get_vendor_history(vendor_name)
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(anomalies, summary, historical_trend)
        
        return {
            "anomaly_detected": len(anomalies) > 0,
            "anomaly_types": anomalies,
            "anomaly_reason": anomaly_reason or "No significant anomalies detected",
            "pattern": pattern_type,
            "risk_score": round(risk_score, 2),
            "historical_trend": historical_trend,
            "fraud_indicators": self._identify_fraud_indicators(anomalies, summary)
        }
    
    def _get_vendor_history(self, vendor_name: str) -> str:
        """Get vendor's historical anomaly trend"""
        normalized_name = utils.normalize_name(vendor_name)
        
        if normalized_name in self.vendor_history:
            history = self.vendor_history[normalized_name]
            count = history.get("anomaly_count", 0)
            total = history.get("total_submissions", 0)
            
            if total > 0:
                return f"Vendor {vendor_name} has {count} prior discrepancies in last {total} submissions"
        
        return f"No prior history for vendor {vendor_name}"
    
    def _calculate_risk_score(self, anomalies: List[str], summary: Dict, history: str) -> float:
        """Calculate risk score (0-10)"""
        score = 0.0
        
        # Base score from anomalies
        score += len(anomalies) * 1.5
        
        # Severity multipliers
        if "vendor_mismatch" in anomalies:
            score += 3.0
        if "significant_overbilling" in anomalies:
            score += 2.5
        if "price_manipulation" in anomalies:
            score += 2.0
        if "suspicious_document" in anomalies:
            score += 1.5
        
        # Discrepancy level
        if summary["discrepancy_level"] == "high":
            score += 2.0
        elif summary["discrepancy_level"] == "medium":
            score += 1.0
        
        # Confidence penalty
        if summary["invoice_confidence"] < 0.5:
            score += 1.5
        
        # Historical pattern (would be enhanced with real data)
        if "prior discrepancies" in history:
            score += 1.0
        
        return min(score, 10.0)
    
    def _identify_fraud_indicators(self, anomalies: List[str], summary: Dict) -> List[str]:
        """Identify specific fraud indicators"""
        indicators = []
        
        if "vendor_mismatch" in anomalies:
            indicators.append("Vendor name does not match PO")
        
        if "significant_overbilling" in anomalies:
            indicators.append("Invoice amount significantly exceeds PO")
        
        if "price_manipulation" in anomalies:
            indicators.append("Unit prices altered from PO")
        
        if not summary["po_number_match"]:
            indicators.append("PO number mismatch or missing")
        
        if summary["invoice_confidence"] < 0.5:
            indicators.append("Low confidence in invoice data extraction")
        
        if not summary["currency_match"]:
            indicators.append("Currency mismatch between documents")
        
        return indicators
    
    def _generate_visualization_data(self, po: Dict, invoice: Dict, 
                                     validation: Dict, anomalies: Dict) -> Dict[str, Any]:
        """Generate data for dashboard visualizations"""
        
        po_total = po.get("total_amount", 0) or 0
        inv_total = invoice.get("total_amount", 0) or 0
        
        # Bar chart: PO vs Invoice totals
        bar_chart = {
            "labels": ["PO Total", "Invoice Total"],
            "values": [round(po_total, 2), round(inv_total, 2)],
            "currency": invoice.get("currency", "INR")
        }
        
        # Pie chart: Discrepancy breakdown
        discrepancy_breakdown = {
            "Tax": 0,
            "Amount": 0,
            "Vendor Name": 0,
            "Quantity": 0,
            "Price": 0,
            "Other": 0
        }
        
        for disc in validation.get("discrepancies", []):
            disc_type = disc.get("type", "")
            if "tax" in disc_type:
                discrepancy_breakdown["Tax"] += 1
            elif "total" in disc_type or "amount" in disc_type:
                discrepancy_breakdown["Amount"] += 1
            elif "vendor" in disc_type:
                discrepancy_breakdown["Vendor Name"] += 1
            elif "quantity" in disc_type:
                discrepancy_breakdown["Quantity"] += 1
            elif "price" in disc_type:
                discrepancy_breakdown["Price"] += 1
            else:
                discrepancy_breakdown["Other"] += 1
        
        pie_chart = {
            "discrepancy_breakdown": discrepancy_breakdown
        }
        
        # Line items comparison
        line_items_comparison = self._compare_line_items(po, invoice)
        
        # Naughty list score (0-10)
        naughty_score = anomalies.get("risk_score", 0)
        
        # Timeline data
        timeline = self._generate_timeline(po, invoice)
        
        return {
            "bar_chart": bar_chart,
            "pie_chart": pie_chart,
            "line_items_comparison": line_items_comparison,
            "naughty_list_score": naughty_score,
            "timeline": timeline,
            "discrepancy_count": validation.get("discrepancy_count", 0),
            "high_severity_count": validation.get("high_severity_count", 0)
        }
    
    def _compare_line_items(self, po: Dict, invoice: Dict) -> List[Dict]:
        """Compare line items between PO and Invoice"""
        comparison = []
        
        po_items = po.get("line_items", [])
        inv_items = invoice.get("line_items", [])
        
        for po_item in po_items:
            po_desc = po_item.get("description", "").lower()
            matched = False
            
            for inv_item in inv_items:
                inv_desc = inv_item.get("description", "").lower()
                
                if utils.fuzzy_match(po_desc, inv_desc, 0.7):
                    matched = True
                    comparison.append({
                        "description": po_item.get("description"),
                        "po_qty": po_item.get("quantity"),
                        "invoice_qty": inv_item.get("quantity"),
                        "po_price": po_item.get("unit_price"),
                        "invoice_price": inv_item.get("unit_price"),
                        "qty_match": po_item.get("quantity") == inv_item.get("quantity"),
                        "price_match": abs((po_item.get("unit_price", 0) or 0) - 
                                         (inv_item.get("unit_price", 0) or 0)) < 0.01
                    })
                    break
            
            if not matched:
                comparison.append({
                    "description": po_item.get("description"),
                    "po_qty": po_item.get("quantity"),
                    "invoice_qty": None,
                    "po_price": po_item.get("unit_price"),
                    "invoice_price": None,
                    "qty_match": False,
                    "price_match": False,
                    "status": "missing_in_invoice"
                })
        
        return comparison
    
    def _generate_timeline(self, po: Dict, invoice: Dict) -> Dict[str, Any]:
        """Generate timeline data for visualization"""
        events = []
        
        if po.get("invoice_date"):
            events.append({
                "date": po["invoice_date"],
                "event": "PO Created",
                "document": "Purchase Order"
            })
        
        if invoice.get("invoice_date"):
            events.append({
                "date": invoice["invoice_date"],
                "event": "Invoice Issued",
                "document": "Invoice"
            })
        
        if invoice.get("due_date"):
            events.append({
                "date": invoice["due_date"],
                "event": "Payment Due",
                "document": "Invoice"
            })
        
        # Sort by date
        events.sort(key=lambda x: x["date"] if x["date"] else "9999-99-99")
        
        return {
            "events": events,
            "total_days": self._calculate_timeline_span(events)
        }
    
    def _calculate_timeline_span(self, events: List[Dict]) -> Optional[int]:
        """Calculate total days in timeline"""
        dates = [e["date"] for e in events if e["date"]]
        if len(dates) >= 2:
            try:
                start = datetime.fromisoformat(min(dates))
                end = datetime.fromisoformat(max(dates))
                return (end - start).days
            except:
                pass
        return None


def verify_from_text(po_text: str, invoice_text: str, 
                     po_filename: str = "PO.pdf", 
                     invoice_filename: str = "Invoice.pdf") -> Dict[str, Any]:
    """
    Convenience function to verify from raw OCR text
    
    Args:
        po_text: Raw OCR text from PO
        invoice_text: Raw OCR text from Invoice
        po_filename: PO filename
        invoice_filename: Invoice filename
    
    Returns:
        Verification result JSON
    """
    agent = VerificationAgent()
    
    po_data = {
        "file_name": po_filename,
        "extracted_text": po_text
    }
    
    invoice_data = {
        "file_name": invoice_filename,
        "extracted_text": invoice_text
    }
    
    return agent.verify_documents(po_data, invoice_data)


def verify_from_parsed(po_parsed: Dict, invoice_parsed: Dict) -> Dict[str, Any]:
    """
    Convenience function to verify from already parsed documents
    
    Args:
        po_parsed: Parsed PO data
        invoice_parsed: Parsed invoice data
    
    Returns:
        Verification result JSON
    """
    agent = VerificationAgent()
    return agent.verify_documents(po_parsed, invoice_parsed)
